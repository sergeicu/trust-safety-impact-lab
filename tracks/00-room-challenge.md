# Room challenge (wildcard)

The evening opens with three short talks and a room full of people who have their own worries about AI in this city. Some of what comes up will not fit tracks 1–5. This slot is for those: take a concern from the room and build on it with the same datasets.

Organizers paste concerns raised during the talks into [`notes/room-concerns.md`](../notes/room-concerns.md) just before 7:00.

## Turn a concern into a challenge (5 minutes)

Write one sentence in this form:

> How might we protect **[who]** from **[what failure]** when **[situation]**, and how would we know it worked (**[signal we can measure tonight]**)?

Then check three things:
1. **Is there data?** Find a dataset in `datasets/catalog.json` that contains examples of the failure or the situation. If there is none, the fastest substitute is 100 cases written by the team and Claude together, clearly labeled synthetic.
2. **Is there a number?** Decide the one measurement before building.
3. **Does it fit in an hour?** One screen, one dataset, one number. Cut until it does.

## Concern-to-data map

| If the room says | Start from |
|---|---|
| "My agent will do something I didn't ask for" | Track 1: `llmail-inject`, `injecagent`, `agentdojo` |
| "Chatbots say harmful things / refuse everything" | Track 1E: `jbb-behaviors`, `aegis-2`, `toxic-chat` |
| "AI treats people differently" | `anthropic-discrim-eval` |
| "Robotaxis and pedestrians, cyclists, emergency vehicles" | Track 3: `nhtsa-sgo-ads`, `ca-av-collisions-zenodo`, `sf-311-cases` |
| "Robots on the sidewalk" | Track 3D: `sf-sidewalk-robot-rules` |
| "Cameras and plate readers everywhere" | Track 4: `eff-atlas-of-surveillance`, `sf-surveillance-inventory` |
| "My data ends up in a model" | Track 4C: `nemotron-pii` |
| "Scams, deepfakes, voice cloning" | Track 5: `uci-sms-spam`, `ftc-consumer-sentinel`, `ai-incident-database` |
| "One of the agents might be working against us" | Track 2: `amongus-sandbox`, `starters/rogue_agent` |
| "Nobody is accountable when AI fails" | `ai-agent-index`, `ai-incident-database`, `mit-ai-risk-repository` |
| "Is this image or video real?" | Track 5E: `c2pa-tools` |
| "Attackers move at AI speed" | Track 1D: `cisa-kev` |
| "What do ordinary people think about AI at work?" | `anthropic-interviewer` |
| "What values should an assistant have?" | `anthropic-values-in-the-wild` |

## Two ready-made wildcard builds

**Concern map of the room.** Take the raw concerns in `notes/room-concerns.md`, classify each against the MIT AI Risk Repository domains (`mit-ai-risk-repository`), and for each one retrieve the three most similar real incidents from the AI Incident Database. Output: a one-page map of what this room worries about, backed by cases. Measure: share of concerns with at least one matching real incident.

**Do the worries match?** Sample 100 transcripts from `anthropic-interviewer`, have Claude extract every trust or safety concern people raise about AI, and compare the distribution with the room's list. Measure: top five concerns in each, and what the room raised that the interviews did not.

`python scripts/fetch.py --track 0` pulls the interview and values samples.
