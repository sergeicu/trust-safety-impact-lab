#!/usr/bin/env python3
"""Fetch hackathon datasets listed in datasets/catalog.json.

Standard library only. Pulls small samples by default so the hour is spent
building, not downloading.

  python scripts/fetch.py --list
  python scripts/fetch.py --track 2
  python scripts/fetch.py --id nhtsa-sgo-ads
  python scripts/fetch.py --id llmail-inject --rows 2000
  python scripts/fetch.py --id sf-311-cases --param '$q=waymo' --param '$limit=500'

Output goes to data/<dataset-id>/. Set HF_TOKEN for gated Hugging Face datasets.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "datasets", "catalog.json")
HF_API = os.environ.get("HF_ROWS_BASE", "https://datasets-server.huggingface.co")
UA = {"User-Agent": "impact-lab-fetch/1.0"}
PAGE = 100  # the dataset viewer API returns at most 100 rows per call


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def open_url(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    return urllib.request.urlopen(req, timeout=timeout)


def get_json(url, headers=None):
    with open_url(url, headers) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_http(spec, out_dir, max_mb):
    names = spec.get("filenames") or []
    for i, url in enumerate(spec["urls"]):
        name = names[i] if i < len(names) else os.path.basename(urllib.parse.urlparse(url).path) or f"file_{i}"
        dest = os.path.join(out_dir, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            log(f"  have {name}, skipping")
            continue
        log(f"  GET {url}")
        cap = max_mb * 1024 * 1024
        got = 0
        tmp = dest + ".part"
        with open_url(url, timeout=120) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                got += len(chunk)
                if got > cap:
                    f.close()
                    os.remove(tmp)
                    raise RuntimeError(f"{name} is larger than --max-mb {max_mb}; rerun with a higher cap if you want it")
                f.write(chunk)
        os.replace(tmp, dest)
        log(f"  saved {dest} ({got / 1e6:.1f} MB)")


def fetch_hf_rows(spec, out_dir, rows_override):
    ds = spec["dataset"]
    headers = {}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["HF_TOKEN"]
    config, split = spec.get("config"), spec.get("split")
    if not config or not split:
        info = get_json(f"{HF_API}/splits?dataset={urllib.parse.quote(ds, safe='')}", headers)
        splits = info.get("splits", [])
        if not splits:
            raise RuntimeError(f"no splits reported for {ds}: {info}")
        if config:
            splits = [s for s in splits if s["config"] == config] or splits
        if split:
            splits = [s for s in splits if s["split"] == split] or splits
        config, split = splits[0]["config"], splits[0]["split"]
    want = rows_override or spec.get("rows", 500)
    dest = os.path.join(out_dir, f"{split}_sample.jsonl")
    n = 0
    with open(dest, "w", encoding="utf-8") as f:
        while n < want:
            q = urllib.parse.urlencode({"dataset": ds, "config": config, "split": split,
                                        "offset": n, "length": min(PAGE, want - n)})
            page = get_json(f"{HF_API}/rows?{q}", headers).get("rows", [])
            if not page:
                break
            for item in page:
                f.write(json.dumps(item["row"], ensure_ascii=False) + "\n")
            n += len(page)
    log(f"  saved {n} rows of {ds} [{config}/{split}] to {dest}")
    log(f"  full dataset: pip install datasets; load_dataset('{ds}')")


def fetch_socrata(spec, out_dir, extra_params):
    params = dict(spec.get("params", {}))
    params.update(extra_params)
    url = f"https://{spec['domain']}/resource/{spec['resource']}.json?{urllib.parse.urlencode(params)}"
    log(f"  GET {url}")
    rows = get_json(url)
    dest = os.path.join(out_dir, "rows.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(rows, f)
    log(f"  saved {len(rows)} rows to {dest}")
    if not rows:
        log("  0 rows: loosen the query (--param '$q=...') or inspect the columns first")


def fetch_git(spec, out_dir):
    if os.path.isdir(os.path.join(out_dir, ".git")):
        log("  already cloned, skipping")
        return
    subprocess.run(["git", "clone", "--depth", "1", spec["repo"], out_dir], check=True)


def fetch_one(ds, args):
    spec = ds.get("fetch", {"type": "manual"})
    kind = spec.get("type")
    log(f"[{ds['id']}] {ds['name']}")
    if kind == "manual":
        log(f"  manual step: {spec.get('instructions', 'open the URL')}")
        log(f"  {ds['url']}")
        return "manual"
    out_dir = os.path.join(args.out, ds["id"])
    os.makedirs(out_dir, exist_ok=True)
    try:
        if kind == "http":
            fetch_http(spec, out_dir, args.max_mb)
        elif kind == "hf_rows":
            fetch_hf_rows(spec, out_dir, args.rows)
        elif kind == "socrata":
            fetch_socrata(spec, out_dir, dict(p.split("=", 1) for p in args.param))
        elif kind == "git":
            fetch_git(spec, out_dir)
        else:
            raise RuntimeError(f"unknown fetch type {kind}")
        return "ok"
    except (urllib.error.URLError, RuntimeError, subprocess.CalledProcessError, OSError, ValueError) as e:
        log(f"  FAILED: {e}")
        log(f"  fall back to the page: {ds['url']}")
        return "failed"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="print the catalog and exit")
    ap.add_argument("--track", type=int, help="fetch every dataset tagged with this track")
    ap.add_argument("--id", action="append", default=[], help="fetch one dataset by id (repeatable)")
    ap.add_argument("--rows", type=int, help="row sample size for Hugging Face datasets")
    ap.add_argument("--param", action="append", default=[], help="extra Socrata query parameter, key=value (repeatable)")
    ap.add_argument("--max-mb", type=int, default=200, help="refuse single files larger than this (default 200)")
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "data"), help="output directory (default ./data)")
    args = ap.parse_args()

    with open(CATALOG, encoding="utf-8") as f:
        datasets = json.load(f)["datasets"]

    if args.list:
        for d in datasets:
            tracks = ",".join(str(t) for t in d["tracks"])
            print(f"{d['id']:<32} track {tracks:<6} {d['fetch']['type']:<8} {d['name']}")
        return 0

    chosen = [d for d in datasets if d["id"] in args.id or (args.track is not None and args.track in d["tracks"])]
    unknown = set(args.id) - {d["id"] for d in datasets}
    if unknown:
        log(f"unknown dataset id(s): {', '.join(sorted(unknown))}")
    if not chosen:
        ap.print_help()
        return 2

    results = {}
    for d in chosen:
        results[d["id"]] = fetch_one(d, args)
    log("\nsummary: " + ", ".join(f"{k}={v}" for k, v in results.items()))
    return 1 if all(v == "failed" for v in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
