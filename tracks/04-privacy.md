# Track 4: Privacy

**The concern.** San Francisco has hundreds of license plate readers, city cameras, drones and audio sensors, each governed by a written policy that almost no resident has read. At the same time people paste their lives into AI tools and connect agents to their accounts. The questions are simple and hard to answer: what is collecting data about me here, who can see it, and how long is it kept?

**What a good hour produces.** A tool that makes an existing public record legible, or a privacy control that is measured rather than promised.

## Pick one challenge

### A. What's watching the Bay?
A plain-language explorer of which agencies use which surveillance technology.
- Data: `eff-atlas-of-surveillance` (one CSV for the whole US). Filter to California and the Bay Area counties.
- Build: pick a city or agency, see its technologies as cards: what it is, what it collects, who sells it, the source link. Have Claude write the "what this means for you" line for each technology type once, then reuse it.
- Measure: number of agencies and technologies covered for the nine Bay Area counties; the most common technology; how many records have a source newer than two years.

### B. Policy versus promise
The city publishes a use policy for every surveillance technology. Turn a stack of PDFs into a comparison a person can scan.
- Data: `sf-surveillance-inventory`. Download 6–10 policies (for example the license plate reader policies of SFPD, SFMTA, Airport, Public Works, Rec and Park).
- Build: Claude extracts the same fields from each: purpose, data collected, retention period, who it may be shared with, whether outside agencies get access, audit and reporting requirements. Show a table, flag blanks and vague language.
- Measure: number of policies processed, share that state a concrete retention period, share that name sharing partners. Spot-check every extracted retention period against the PDF.

### C. The PII airlock
A redaction layer that sits in front of a model, a log file or an agent's memory.
- Data: `nemotron-pii` (synthetic documents with labeled PII spans, CC BY 4.0).
- Build: detect and replace names, addresses, phone numbers, account numbers and so on, with consistent placeholders so the text still makes sense. Compare a regex baseline to a Claude-based pass.
- Measure: precision and recall by entity type on 200+ documents. Show which types leak most.

### D. Plate readers by the numbers (stretch)
- Data: `eff-ca-alpr` (scans and hits for 89 California agencies).
- Build: for each agency, how many plates were scanned for each one that matched a hotlist. One chart, sorted.
- Measure: the median hit rate. Note that the data is from 2021 and earlier.

## Data

| id | What it is | Pull |
|---|---|---|
| `eff-atlas-of-surveillance` | Agency-by-technology records with sources, CSV | `python scripts/fetch.py --id eff-atlas-of-surveillance` |
| `sf-surveillance-inventory` | The city's inventory and one policy PDF per technology and department | manual, see catalog |
| `eff-ca-alpr` | California plate reader scan and hit counts | manual |
| `nemotron-pii` | Synthetic text with PII labels | `python scripts/fetch.py --id nemotron-pii` |

`python scripts/fetch.py --track 4` pulls the direct ones.

## One-hour plan

| Minute | Do |
|---|---|
| 0–10 | Fetch the Atlas CSV (A), or download 6 policy PDFs (B), or the PII sample (C). Print what you have. |
| 10–25 | Thin path on 5 records, policies or documents. Fix the schema now, not later. |
| 25–40 | Scale up. Cache every model response. |
| 40–50 | Compute the numbers. Hand-check the ones you will say out loud. |
| 50–60 | `SUBMISSION.md`, run command, one example to show. |

## Watch out for

- The Atlas is open-source research compiled from news, public records and vendor material. An agency missing from it has not been shown to use nothing.
- Stay at the level of agencies and technologies. Mapping exact camera locations or helping anyone evade or target a device is out of scope.
- Policy PDFs differ in format. Expect a couple to defeat text extraction; skip them and say so.
- Extraction models make confident mistakes on numbers. Check every retention period and date you display.
- For redaction demos use synthetic text only. Do not paste your own inbox on the projector.

## Demo checklist

One real record or policy on screen. Your tool making it understandable. One number with its sample size. One gap in the public record.
