# Claude Impact Lab SF: Trust & Safety Micro-Hack

Robotaxis fill the streets. AI agents read our inboxes. Robots are showing up on the sidewalk. Who is building the guardrails?

This repo is the working kit for the evening: five build tracks, the public datasets behind each one, and instructions written so that a coding agent (Claude Code or similar) can go from "pick a track" to a working demo in about 60 minutes.

**If you are an agent, read [`AGENTS.md`](AGENTS.md) first.** Everything you need is in this repo.

> A Claude Community Event in San Francisco, hosted by official Claude Ambassadors, with Antler. Date, venue and RSVP: see the Luma page.

## The evening

| Time | What happens |
|---|---|
| 6:00 – 6:30 | Registration, food, find a team |
| 6:30 – 7:00 | Three 10-minute talks |
| 7:00 – 8:00 | **Hack.** Teams pick a track, point their agent at this repo, and build. |
| 8:00 – 8:15 | Hands off keyboards, fill in `SUBMISSION.md`, line up demos |
| 8:15 – 9:00 | Presentations, about 3 minutes per team |
| 9:00 – 10:00 | Overflow demos and social |

One hour of building is short. The tracks are scoped so that an agent does most of the typing while the humans steer, check the output, and prepare the demo. Every track comes with public data that can be pulled in minutes.

## The tracks

| # | Track | The question | Main data |
|---|---|---|---|
| 1 | [Agents in Inboxes](tracks/01-agents-in-inboxes.md) | An agent reads my email. What stops a stranger's email from giving it orders? | LLMail-Inject, InjecAgent, AgentDojo, CISA KEV |
| 2 | [Spot the Rogue Agent](tracks/02-spot-the-rogue-agent.md) | In a team of agents, one goes rogue. Can the others find it and shut it out? | Starter game in this repo, Among Us agent logs |
| 3 | [Robotaxis & Robots](tracks/03-robotaxis-and-robots.md) | How safe are robotaxis here, and what is nobody reporting? | NHTSA crash reports, CA DMV, CPUC, DataSF |
| 4 | [Privacy](tracks/04-privacy.md) | What surveillance tech covers my city, and where does my data go? | EFF Atlas of Surveillance, SF Surveillance Technology Inventory, Nemotron-PII |
| 5 | [Personal Safety](tracks/05-personal-safety.md) | AI made scams and fakes cheap. How do my parents tell what is real? | FTC fraud data, SMS and phishing corpora, AI Incident Database, C2PA tools |
| 0 | [Room challenge](tracks/00-room-challenge.md) (wildcard) | A concern from the room that does not fit 1–5 | Mapped to the same datasets |

Every track file has the same shape: the concern, starter challenges sized for one hour, the datasets with pull commands, a minute-by-minute plan, the traps in the data, and a demo checklist.

## Quick start

```bash
git clone <this-repo> && cd <this-repo>
export ANTHROPIC_API_KEY=...        # credits are handed out at the event

python scripts/fetch.py --list       # every dataset in the catalog
python scripts/fetch.py --track 3    # pull the small, direct-download data for track 3
python starters/rogue_agent/sim.py --mock   # track 2 needs no download at all
```

Then tell your agent:

> Read AGENTS.md and tracks/03-robotaxis-and-robots.md. We are doing challenge A. You have 55 minutes. Start now.

`scripts/fetch.py` uses only the Python standard library. It pulls small samples by default so nobody spends the hour downloading.

## What you hand in

By 8:15, each team has:

1. Something that runs: a page, a notebook, a CLI, a bot.
2. A filled-in [`SUBMISSION.md`](SUBMISSION.md) (six short answers, including who is accountable when your thing fails).
3. A 3-minute demo: the concern, the thing working on real data, one honest limitation.

## Repo map

```
AGENTS.md              instructions for coding agents (CLAUDE.md points here)
SAFETY.md              ground rules for working with attack, abuse and personal data
SUBMISSION.md          what each team hands in
tracks/                one file per track
datasets/catalog.json  machine-readable dataset catalog (used by scripts/fetch.py)
datasets/README.md     the same catalog as a table, with licenses and caveats
scripts/fetch.py       dataset fetcher (stdlib only)
starters/rogue_agent/  the imposter game for track 2 (runs without an API key in --mock mode)
notes/room-concerns.md organizers paste concerns from the room here at ~6:55
submissions/           teams add their SUBMISSION.md here by pull request
```

## No coding experience?

You are still useful on a team. Someone has to decide which concern matters, read what the agent produces and say "that is wrong", write the plain-language explanation, and give the demo. Challenges 3A, 4A, 4B and 5A are the most approachable.

## About

Claude Impact Labs put builders to work on real problems in their own city and keep the best ideas moving after the demos. Free, like every Claude Community event. Promising teams can talk with [Antler](https://www.antler.co/) about its residency and investor network (no acceptance or investment is promised).

Code in this repo is MIT licensed. Datasets keep their own licenses; see [`datasets/README.md`](datasets/README.md).
