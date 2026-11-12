# Track 5: Personal Safety

**The concern.** AI has made convincing lies cheap: a text that sounds like your bank, a voice that sounds like your kid, a job offer written in perfect English or perfect Cantonese. The people most exposed are often the least likely to be at a hackathon. Personal safety here means the everyday version: not getting robbed by a message, and getting information about your own neighborhood that you can trust.

**What a good hour produces.** Something a non-technical person could use tonight, with its accuracy measured and its limits stated.

## Pick one challenge

### A. "Is this a scam?"
Paste a message, get a verdict, the specific red flags, and what to do next.
- Data: `uci-sms-spam` and `phishing-multi` for labeled messages.
- Build: a one-screen checker. Output in the reader's language: test at least English, Chinese and Spanish. The explanation matters as much as the label: "it asks you to move money to keep it safe; banks do not do that".
- Measure: accuracy, missed-scam rate and false-alarm rate on 200+ labeled messages. Then try five current-style scams the team writes or has received and report those separately.
- Next step text should point to real channels: reportfraud.ftc.gov, the bank's number on the back of the card.

### B. Scam weather report
What is hitting the Bay Area right now, and who is losing money?
- Data: `ftc-consumer-sentinel` (annual Data Book CSVs, including metro-area tables), plus `ai-incident-database` filtered to fraud, impersonation and deepfake incidents.
- Build: a one-page brief: top fraud categories and losses for California and the San Francisco metro area, year over year, with three short "how it works" cards built from AI Incident Database cases.
- Measure: the category with the largest reported losses, the year-over-year change, the number of AI-related fraud incidents found and their date range.

### C. Lessons from AI fraud incidents
- Data: `ai-incident-database` (take the small Excel export), `mit-ai-risk-repository` for the label set.
- Build: pull incidents about voice cloning, deepfake video calls, AI-written phishing and chatbot impersonation. Claude codes each one: target, channel, what made it convincing, what would have stopped it. Turn the "what would have stopped it" column into a family or small-business checklist (safe word, call-back rule, payment hold).
- Measure: number of incidents coded, top three preventable patterns with counts.

### D. Honest neighborhood brief (stretch)
Safety apps tend to sell fear. Build the calm version.
- Data: `sfpd-incident-reports` (public, daily).
- Build: pick a neighborhood, show trends by category over 24 months with plain-language context: is this up or down, how does it compare with the city, what the data does and does not include.
- Measure: month-over-month and year-over-year change with counts. Aggregate only: neighborhood and month, never individual incidents on a map.

### E. Provenance reader (stretch)
People cannot tell real photos from generated ones, and detectors are unreliable. Provenance is the other approach: signed metadata saying where a file came from.
- Data: `c2pa-tools` (open-source Content Credentials tooling) and a handful of images with and without credentials that the team collects.
- Build: drop in an image, get a plain-language answer: who signed it, what tool made it, what was edited, or "no credentials, which proves nothing either way".
- Measure: of N images tested, how many carried credentials and how many survived a screenshot or a re-upload. Do not claim to detect fakes.

## Data

| id | What it is | Pull |
|---|---|---|
| `uci-sms-spam` | 5,574 labeled SMS messages, CC BY 4.0 | `python scripts/fetch.py --id uci-sms-spam` |
| `phishing-multi` | Phishing vs. benign emails, SMS, URLs, pages | manual (download the JSON files) |
| `ftc-consumer-sentinel` | FTC fraud report aggregates by category, state, metro | manual (small CSV zip) |
| `ai-incident-database` | Press-reported AI incidents with linked reports | manual (small Excel export) |
| `mit-ai-risk-repository` | Risk taxonomy and incident classifications | manual |
| `c2pa-tools` | Open-source Content Credentials (C2PA) tools | manual |
| `sfpd-incident-reports` | SFPD incident reports since 2018, Socrata API | `python scripts/fetch.py --id sfpd-incident-reports` |

`python scripts/fetch.py --track 5` pulls the direct ones.

## One-hour plan

| Minute | Do |
|---|---|
| 0–10 | Fetch the SMS set (A) or download the FTC zip and AIID export (B, C). Print samples. |
| 10–25 | Thin path: 50 messages classified with explanations, or 20 incidents coded. |
| 25–40 | Scale to 200+. Add the second language or the second data source. |
| 40–50 | Compute the numbers. Read 10 explanations aloud to a teammate: would your aunt understand them? |
| 50–60 | `SUBMISSION.md`, run command, pick the one example to demo. |

## Watch out for

- The SMS corpus is from 2012 and not from the US. A high score on it says little about this year's scams. Say that, and show your handful of current examples next to it.
- FTC numbers are self-reported complaints. Older adults report less often and lose more per report; under-reporting is large everywhere.
- A scam checker that says "safe" is giving advice. Prefer three outputs: likely scam, cannot tell, no red flags found. Never tell someone a message is definitely legitimate.
- Build detectors and explainers. Do not generate send-ready scam scripts or clone a real person's voice, even to make the demo vivid.
- Police incident data reflects what was reported and recorded. It is not a measure of how safe a block is, and category definitions matter.

## Demo checklist

One real message or incident on screen. Your tool explaining it in plain language. Accuracy numbers with sample size. One kind of scam it misses.
