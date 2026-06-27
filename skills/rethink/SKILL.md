---
name: rethink
description: Use when you're about to "add a rule so the AI won't do that again" — after a mistake, a correction, or any "update your instructions to prevent this" request. Instead of bolting another negative prohibition onto your instructions, this skill forces root-cause analysis, converts the ban into a positive process, routes it to the right layer (hook / skill / memory / project instructions), and audits your instruction file for bloat. Triggers on "/rethink", "add a rule so you don't…", "make sure you never…", "remember not to…", or any moment the thought "I'll just add a don't-do-that note" appears.
---

# /rethink — route a mistake to the right fix, not another ban

## The problem this solves

When an AI agent makes a mistake, the reflex is to add a line to its instructions:
*"Never do X."* It feels like progress. It isn't.

A negative rule is a one-time patch. Next time the agent fails with Y or Z instead —
same root cause, different surface — and you add another ban. Your instruction file
swells with "don't do this" notes, each one spending context budget on every single
request, while the underlying structural gap is never closed.

**This skill stops that.** When you're tempted to add a prohibition, run this first.

## The rule

**"I'll add a rule so it won't happen again" is never the immediate action.**
Run this skill first, then decide where (and whether) anything gets written.

Correct order for fixing a mistake:
1. **Root-cause analysis** (symptom → direct cause → structural cause)
2. **Negative → positive conversion** (turn the ban into an enabling process)
3. **Layer routing** (decide where it belongs — or that it belongs nowhere)
4. **Write + audit** (apply it, then check the instruction file for debt)

---

## Phase 1 — Root-cause analysis (REQUIRED)

Answer all six before moving on. Q3 and Q6 are the ones that matter — stopping at
Q1/Q2 is symptom-patching, not structural improvement.

- **Q1. Symptom** — What exactly went wrong? (concrete behavior)
- **Q2. Direct cause** — Why did the agent do that? (the in-the-moment decision)
- **Q3. Upstream cause** — Why did it *decide* that? What in the system, context, or
  instructions made that decision look correct?
- **Q4. Class** — Pick one category (see Phase 1.5 table). If it's ambiguous, prefer
  the *narrower* scope.
- **Q5. Recurrence** — One-off / pattern / chronic?
- **Q6. Structural flaw** — State, in 1–2 sentences, the system weakness this mistake
  reveals.

---

## Phase 1.5 — Negative → positive conversion (HARD GATE)

> Pass this before Phase 2. This gate is what blocks the "pile up bans" anti-pattern.

**Adding a negative prohibition ("never do B") to any layer is forbidden here.**
A ban is a single-use shield — next time it leaks through C or D, the instructions
bloat, and the root structure is untouched. Convert in three steps.

**G1. Abstract the category.** Treat the mistake as a *type*, not an incident.

| Category | Definition | Positive conversion direction |
|---|---|---|
| Wrong selection | Chose B when A was right (wrong target/option) | A compare-and-verify gate before deciding |
| Sequence error | Skipped a step or did them out of order | A fixed checklist / ordering |
| Priority failure | Did the important thing late or not at all | Apply a priority frame first |
| Context blindness | Misread the session, state, or instructions | A context-check gate before starting |

**G2. Sibling failures.** In the same category, would C, D, E also be prevented — or
only B? If your fix only blocks B, the conversion isn't done.

**G3. Convert to a positive process.** Write a gate that *opens* the right behavior,
not a prohibition that *closes* a wrong one.
- ❌ "Never do B" → ✅ "Before deciding, check A's condition and state the result, then proceed"
- ❌ "Never guess" → ✅ "If unsure, say so, then search N times; if still unknown, ask the user"
- Only adopt a structure that prevents the *whole category* at once.

**Escape hatch:** if even a positive process is overkill for a genuine one-off, mark
Q4 as one-off and make Phase 2 a no-op. *Choosing to write nothing is a valid result.*

> Output of this phase: **one converted positive-process sentence** (or a no-op
> verdict). That sentence — never a ban — is the input to Phase 2.

See [references/positive-process-examples.md](references/positive-process-examples.md)
for worked conversions.

---

## Phase 2 — Layer routing

Decide where the positive process belongs. Match the diagnosis to the **narrowest
layer that actually fixes it**:

| Layer | Use when | How |
|---|---|---|
| **Hook** (deterministic) | The behavior must fire automatically every time, not be remembered | Add a hook that injects the gate at the right event |
| **New skill** | It's a reusable procedure worth its own trigger | Author a skill |
| **Existing skill** | It belongs to a procedure you already have | Edit that skill |
| **Memory / notes** | It's a fact or preference to recall, not a procedure | Append to your memory file |
| **Project instructions** (e.g. CLAUDE.md / AGENTS.md) | It genuinely applies to *every* request in this project | Insert into the most specific section |
| **Nothing** | One-off, or no structural fix is warranted | Log it and stop |

**Before choosing project-wide instructions, ask:** "Does this *really* apply to
every session and every request? Is there no narrower layer it could live in?" If you
can't answer yes, don't put it there. Global instruction files are the most expensive
layer — every line is re-read on every request.

Present 1–2 candidate layers and pick. "Nowhere" is always a legitimate candidate.

---

## Phase 3 — Write + audit + log

**A. Write to the chosen layer.** Apply the positive process — never a bare ban.

**B. Audit the instruction file.** While you're here, scan your project-wide
instructions for prior rules on the *same topic*. Hooks and skills accrete; bans
especially. There's a tiny helper for this — point it at your instruction file and it
counts the negative rules and flags topics that already have multiple bans:

```bash
python3 ~/.claude/skills/rethink/audit.py CLAUDE.md
# → "Negative rules found: 14" + "Topics with multiple bans: 3× config, 2× commit"
```

It's a thermometer, not a doctor: it shows where bans are piling up; you still run
rethink on each cluster to convert them into one positive gate. If you find duplication,
contradiction, or a rule that should move to a narrower layer, flag it. **Never
auto-delete without the user's approval.**

**C. Log the change** (optional but recommended). Keep a short changelog entry so the
evolution of your agent's instructions is traceable:

```markdown
### [CHG-N] YYYY-MM-DD — <title>
- Class: <category from Phase 1.5>
- Recurrence: <one-off | pattern | chronic>
- Target: <file/layer changed>
- Change type: <add | move-layer | delete | new-skill | new-hook | no-op>
- Structural cause: <Q3 / Q6 summary>
- What changed: <one line>
```

### Done

End with a one-line summary, e.g.:
```
[rethink] wrong-selection → routed to a pre-decision check hook. Logged CHG-12.
```

---

## When to reach for deusex instead

`rethink` is for **the agent's own mistakes** — it ends in a routing decision (hook /
skill / memory / instructions). When the problem is a **structural flaw in code, a
system, or a workflow** rather than the agent's behavior, use
[deusex](../deusex/SKILL.md), which ends in an architectural redesign. They share the
same spine: never patch a symptom before you've found its structural cause.
