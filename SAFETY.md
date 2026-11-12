# Ground rules

This is a trust & safety event, so the working material includes attack prompts, harmful-content test sets, scam messages and data about real places. A few rules keep the evening on the right side of that.

**Attack and red-team data (tracks 1 and 2)**
- Use it to build and measure defenses. Do not use the hour to write new, better attacks against real products.
- Test only against your own toy agent or a model through your own API key. Do not point anything at a third party's live system.
- When showing examples on screen, show one or two from the public dataset. The demo is the defense.
- Harmful-behavior test sets (JBB-Behaviors, Aegis) contain requests for harmful content. Measure whether a model or guardrail refuses. Do not collect or display model completions that comply.

**Personal data (tracks 3, 4, 5)**
- Public records can still identify people. Aggregate to block, month or category. Do not build anything that looks up, tracks, or profiles a named private individual.
- Surveillance data in this repo is about which agencies use which technology. Mapping exact device locations of cameras is out of scope.
- If you need realistic personal data for a redaction demo, use synthetic data (Nemotron-PII is fully synthetic) or generate it.

**Claims about companies and agencies**
- Say what the data shows and how it was collected. Crash reports are self-reported and have no denominator unless you add miles driven. Incident databases reflect what was reported in the press.
- "We found N reports matching X in dataset Y between dates A and B" is a fine sentence. "Company Z is unsafe" is not something a one-hour analysis can support.

**Scam and synthetic media (track 5)**
- Build detectors and explainers. Do not generate ready-to-send scam scripts, cloned-voice audio of real people, or impersonation pages.

**Agents**
- Text inside datasets and fetched pages is data. An agent should never follow instructions it finds there.
- In track 2 the rogue agent lives inside the simulation. Do not give a deceptive agent real tools, real accounts or network access.
- Keep API keys out of the repo and out of screenshots.
