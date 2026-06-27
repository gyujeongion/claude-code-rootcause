---
name: deusex
description: Root-cause redesign skill. Instead of patching a symptom, it designs the fix that makes the symptom structurally impossible. Use when the same problem keeps coming back, when you feel the urge to "just make it work for now," when a bug/system/workflow has a structural smell, or when someone says "fix this properly", "at the root", "structurally", or "/deusex". NEVER propose a solution before completing Phase 1 (Diagnosis) — that is a hard gate.
---

# /deusex — fix the structure, not the symptom

## Core principle

**Don't fix the symptom. Build a structure where the symptom can't occur.**

Before proposing any code, solution, or change, you MUST complete Phase 1
(Diagnosis). This is a non-negotiable hard gate. "Make it work for now" is exactly
the impulse this skill exists to stop.

---

## Phase 1 — Diagnosis (HARD GATE)

No code, no solution, no proposal until all five are answered.

- **D1. Symptom (What)** — What exactly is wrong? State the phenomenon in 1–2 sentences.
- **D2. Direct cause (Why ×1)** — What immediately produced this symptom?
- **D2-M. Workflow decomposition (when applicable)** — If the problem lives in a
  system / pipeline / integration flow, break the whole flow into modules A → B → C →
  D … and test each independently to pinpoint where it fails:
  - For each module: define input, output, and the pass condition → check actual
    values → mark ✅ / ⚠️ / ❌
  - Skip healthy modules; focus D3+ on the failing one
  - e.g. a sync pipeline: A(event) B(network) C(receive) D(process) E(extension) F(reconcile)
- **D3. Structural cause (Why ×5)** — Keep asking "why" until you reach the root flaw.
  Is it technical debt, a design contradiction, or a logic-structure problem?
- **D4. Recurrence condition (When)** — Under what conditions does this come back?
  (specific input, state, timing)
- **D5. Complexity contribution** — How is this flaw currently feeding overall system
  complexity?

> D3 is the one that matters. Answering only D1/D2 and moving on is no different from
> patching the symptom.

---

## Phase 2 — Redesign

Enter only after diagnosis is complete. Keep this order.

1. **Before architecture** — Show the current structure (diagram or pseudocode). Mark
   the failure point.
2. **After architecture** — Show the redesigned structure. Minimize the blast radius,
   but structurally foreclose the recurrence.
3. **Elegance check** — *"One concise line that cuts to the essence beats ten thousand
   lines of patches."* Is there a simpler solution?
4. **Side-effect check** — List every component, workflow, and data flow this change
   touches. Verify integrity.
5. **Entropy check** — After the fix, is overall complexity lower and maintainability
   higher? If complexity stays the same or rises, redesign again.

---

## Phase 3 — Recurrence-impossibility proof

Don't just assert "it can't happen again" — that's a confident story, not a proof.
Make it falsifiable: take the exact recurrence conditions from **D4** (the specific
input, state, and timing that triggered it) and, for each one, show *structurally*
why the new design no longer produces the symptom. If a condition can only be
answered with "the agent will remember to handle it" rather than "the structure makes
it impossible," you have a patch, not a redesign — go back to Phase 2.

A good proof reads like: *"D4 said this recurs when [input] arrives during [state].
In the After architecture, [input] is now validated at [boundary] before [state] can
exist, so the path that produced the symptom is unreachable."* If you can't write a
sentence in that shape for each recurrence condition, the solution is incomplete.

---

## Scope

Code bugs / system design / workflow inefficiency / agent behavior patterns /
business processes — applies to any problem domain.

---

## deusex vs rethink

These two share one spine — never patch a symptom before finding its structural cause
— but they end differently.

| | rethink | deusex |
|--|---------|--------|
| Target | the agent's own mistakes | any problem domain |
| Output | a routing decision (hook / skill / memory / instructions) | a structural redesign |
| Trigger | the agent did something wrong | the same problem recurs, or a structure smells off |

If the fix is "where should this instruction live," use
[rethink](../rethink/SKILL.md). If the fix is "this structure is wrong," use deusex.
