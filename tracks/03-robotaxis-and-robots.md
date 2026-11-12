# Track 3: Robotaxis & Robots

**The concern.** San Francisco shares its streets with driverless cars, and delivery robots are testing on its sidewalks. Residents mostly hear two stories: company safety statistics and viral videos. The public record sits in between, spread across a federal crash file, state PDFs, utility-commission spreadsheets and the city's 311 system, and almost nobody reads it.

**What a good hour produces.** Something a resident or a supervisor's aide could open and understand: what has been reported, what the rate looks like when you add miles, and what is not being collected at all.

## Pick one challenge

### A. SF robotaxi report card
A single page built from the federal crash reports, filtered to San Francisco.
- Data: `nhtsa-sgo-ads` (current) and optionally `nhtsa-sgo-ads-archive`.
- Build: reports by month, by operator, by what the vehicle collided with, by highest injury severity. Have Claude rewrite 10 narratives into one plain sentence each.
- Measure: de-duplicated crash count for San Francisco over a stated date range, and the share involving a pedestrian or cyclist.
- Make it honest: put "self-reported, unverified, no mileage" on the page. If you have time, add miles from `waymo-safety-hub` or `cpuc-av-quarterly` and show a rate.

### B. Narrative miner
The interesting information is in the free-text narratives: was the robotaxi moving, who hit whom, was a vulnerable road user involved, did the vehicle stop in a lane.
- Data: `ca-av-collisions-zenodo` (one clean CSV, 2019–2024) or the narrative column of `nhtsa-sgo-ads`.
- Build: a fixed schema (AV moving or stopped; struck or striking; other party type; location type; contributing behavior) filled in by Claude for 100–200 narratives, with a human spot-check of 20.
- Measure: distribution of each field, and your spot-check agreement rate.

### C. The missing-data map
Collisions are reported. Near misses, blocked crosswalks, stalled vehicles in front of fire stations and bus delays mostly are not.
- Data: `sf-311-cases` (the city accepts autonomous vehicle incident reports through 311), `ca-dmv-disengagements`, `cpuc-av-quarterly`.
- Build: a table of "what a resident might experience" versus "which dataset would record it, who files it, and is it public". Then query 311 for what is there. If little or nothing is, design the near-miss report schema you think the city should publish and build the intake form or chat bot for it.
- Measure: number of matching 311 records by month, or, if none, the documented list of fields that no public dataset captures.

### D. Sidewalk robot rules, as code
San Francisco allows sidewalk delivery robots only under testing permits with tight limits.
- Data: `sf-sidewalk-robot-rules` (Public Works Code Sec. 794).
- Build: turn the section into a checklist an operator or a resident can run ("is this robot allowed to be here?"), and a short incident report form for when the answer is no.
- Measure: number of distinct, checkable rules extracted, each linked to its clause.

## Data

| id | What it is | Pull |
|---|---|---|
| `nhtsa-sgo-ads` | Federal crash reports for automated driving systems, June 2025 onward, monthly CSV | `python scripts/fetch.py --id nhtsa-sgo-ads` |
| `nhtsa-sgo-ads-archive` | Same, 2021 to June 2025, older schema | `python scripts/fetch.py --id nhtsa-sgo-ads-archive` |
| `nhtsa-sgo-adas` | Driver-assist (Level 2) crash reports | `python scripts/fetch.py --id nhtsa-sgo-adas` |
| `ca-av-collisions-zenodo` | CA DMV collision reports 2019–2024 as one CSV, CC BY 4.0 | `python scripts/fetch.py --id ca-av-collisions-zenodo` |
| `ca-dmv-collision-reports` | Original PDFs, including 2025–2026 | manual, see catalog |
| `ca-dmv-disengagements` | Yearly disengagement and mileage CSVs (testing permits) | manual |
| `cpuc-av-quarterly` | Passenger-service quarterly data: trips, miles, more | manual |
| `waymo-safety-hub` | Company-published miles and crash data by city | manual |
| `sf-311-cases` | 311 service requests, Socrata API | `python scripts/fetch.py --id sf-311-cases` |
| `sf-traffic-crashes` | All injury crashes in SF (human baseline) | `python scripts/fetch.py --id sf-traffic-crashes` |
| `sf-sidewalk-robot-rules` | City code for sidewalk delivery robots | manual |

`python scripts/fetch.py --track 3` pulls the direct ones.

## One-hour plan

| Minute | Do |
|---|---|
| 0–10 | Fetch the NHTSA CSV and the Zenodo CSV. Print headers. Open the data dictionary PDF for the column you are unsure about. Filter to San Francisco. |
| 10–25 | De-duplicate reports. First chart or first 30 narratives through Claude. |
| 25–40 | Fill out the page or schema. Add the denominator if you are going for a rate. |
| 40–50 | Spot-check 20 rows by hand. Write the caveat box. |
| 50–60 | `SUBMISSION.md`, run command, choose one narrative to read aloud. |

## Watch out for

- **Duplicates.** One crash can have several report versions and several reporting entities. Count crashes, not rows.
- **Schema change.** The NHTSA file format changed in June 2025. The archive and the current file do not share all columns.
- **Redaction.** Some narratives are withheld as confidential business information. Report how many.
- **Testing versus deployment.** California DMV disengagement reports cover testing permits only. Commercial robotaxi service mostly reports to the CPUC instead.
- **Counts are not rates.** More robotaxi crashes in a year with far more robotaxi miles can mean a lower rate. Do not put a bare count next to a safety claim.

## Demo checklist

One real crash narrative, in plain English. Your page or table. One number with its date range and sample size. One thing the public record cannot tell you.
