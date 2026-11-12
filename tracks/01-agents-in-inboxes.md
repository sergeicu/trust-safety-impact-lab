# Track 1: Agents in Inboxes

**The concern.** People are handing AI agents their email, calendar and files. An agent that reads an email cannot reliably tell the difference between content to summarise and an instruction to obey. Anyone who can send you an email can try to give your agent orders: forward this thread, send that file, approve this payment. This is indirect prompt injection, and it is the main reason agent guardrails are hard.

**What a good hour produces.** A defense you can measure: a filter, a policy layer or a field guide, scored on real attack data.

## Pick one challenge

### A. The inbox firewall
Build a layer that sits between "email arrives" and "agent reads it". For each email it returns allow, quarantine or strip, with a reason.
- Data: `llmail-inject` for attacks. For benign email, have Claude write 100 ordinary work emails (meeting moves, invoices, newsletters, forwarded chains), including ones that legitimately contain imperative language ("please send me the report by Friday").
- Measure: attack catch rate and false-positive rate on benign mail, on at least 200 + 100 items. Report both. A filter that blocks everything scores 100% on the first number.
- Good twist: compare a keyword heuristic, a Claude-as-judge prompt, and both together.

### B. Field guide to inbox attacks
Take a few thousand attack emails and turn them into something a defender can read in five minutes.
- Data: `llmail-inject`. The `objectives` field records how far each attack got (retrieved by the assistant, evaded the defense, triggered the send). Parse it and separate attacks that worked from those that did not.
- Build: have Claude label a sample of 300–500 with a tactic (fake system message, pretend conversation turn, urgency or authority, encoding or obfuscation, hidden in a long benign email, other). Show the share of each tactic among successful versus failed attacks, with one short example each.
- Measure: tactic distribution with counts; which tactics are over-represented among successes.

### C. Least-privilege agent
Skip detection and limit the blast radius instead. Write a tiny email agent with three tools (read, search, send) and wrap it in a policy: sending to a new recipient needs confirmation, content that came from an email cannot become the recipient or body of an outgoing message without a human seeing it, and so on.
- Data: `injecagent` test cases (user task + poisoned tool response + attacker goal), or the workspace suite in `agentdojo` if you want a full environment.
- Measure: attack success rate with and without the policy on 50+ cases, plus how many legitimate tasks the policy blocked.

### D. Agent permission audit
Agents hold keys: API tokens, mailbox scopes, file access. Most hold more than their job needs.
- Data: write (with Claude) 20 realistic agent configurations: the job description, the tools and scopes granted. Use `cisa-kev` if you want the "how fast do attackers move" angle: time from a vulnerability being published to it being exploited in the wild.
- Build: an auditor that reads an agent's job and its granted permissions and returns the minimum set, the excess, and the worst thing the excess allows.
- Measure: share of configurations with excess permissions, average number of excess scopes; or, for the KEV angle, median days from disclosure to listing, by year. Label synthetic configurations as synthetic.

### E. Guardrail stress test (stretch)
Does a safety filter block the right things, and only those?
- Data: `jbb-behaviors` (100 harmful + 100 matched benign requests), `aegis-2` test split, `toxic-chat` for realistic mostly-benign traffic.
- Build: run a guard prompt over a sample, show the confusion matrix by category, then revise the prompt once and show the change.
- Measure: missed-harm rate and over-refusal rate. Read `SAFETY.md` first: measure refusals, do not collect harmful completions.
- Advanced: use Bloom (`petri-bloom`) to generate 10–20 scenarios for one behavior such as "agent shares the user's private data when asked nicely by a third party".

## Data

| id | What it is | Pull |
|---|---|---|
| `llmail-inject` | About 462k attacker-written emails from Microsoft's public challenge against a simulated email assistant, MIT license | `python scripts/fetch.py --id llmail-inject --rows 2000` |
| `injecagent` | 1,054 indirect-injection test cases across 17 user tools | `python scripts/fetch.py --id injecagent` |
| `agentdojo` | Full agent environment (workspace, travel, banking, slack suites) | `pip install agentdojo` |
| `deepset-prompt-injections` | Small labeled injection/benign prompt set | `python scripts/fetch.py --id deepset-prompt-injections` |
| `jbb-behaviors`, `aegis-2`, `toxic-chat` | Content-safety test sets | `python scripts/fetch.py --id jbb-behaviors` etc. |
| `cisa-kev` | CISA catalog of vulnerabilities known to be exploited, CC0 | `python scripts/fetch.py --id cisa-kev` |
| `agentharm`, `anthropic-discrim-eval`, `petri-bloom` | Harmful agent tasks, fairness probes, auditing tools | see `datasets/README.md` |

`python scripts/fetch.py --track 1` pulls samples of everything that is directly fetchable.

## One-hour plan

| Minute | Do |
|---|---|
| 0–10 | Fetch `llmail-inject` sample. Print 5 rows. Parse `objectives`. Decide A, B, C, D or E. |
| 10–25 | Thin path: 50 attacks + 50 benign through your filter or labeler, results cached to JSONL. |
| 25–40 | Scale to 300+, add the comparison (second method, or with/without policy). |
| 40–50 | Compute the two numbers, build the one-screen view. |
| 50–60 | `SUBMISSION.md`, one run command, pick the single best example to show. |

## Watch out for

- **Your agent is reading attack emails.** Tell it explicitly that dataset rows are strings to classify, never instructions. If it starts "following" an email, that is a live demonstration of the problem and worth mentioning in the demo.
- The attacks were written against one specific simulated assistant and one target action (sending an email). They are not a sample of what arrives in real inboxes.
- LLM-generated benign email is easier to tell apart from attacks than real email is. Say so next to your false-positive rate.

## Demo checklist

One real attack email on screen. Your defense handling it. Two numbers with sample sizes. One attack that still gets through.
