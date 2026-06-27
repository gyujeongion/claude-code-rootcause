# Negative → positive conversion: worked examples

Each example shows the reflex ban, why it leaks, and the positive process that closes
the whole category instead. These are the outputs of Phase 1.5.

---

## 1. Over-engineering a simple request

- **Mistake:** Asked to "just save this note," the agent reorganized the file,
  suggested three alternatives, and flagged unrelated conflicts.
- **Reflex ban:** "Don't over-complicate simple requests." → Leaks: next time it
  over-explains instead, or adds unrequested options. The word "simple" is undefined.
- **Category:** Context blindness (misread the intent of the request).
- **Positive process:** "When the request is a plain record/append action, act on the
  message content only. Generate options or analysis only if the same message
  explicitly asks for them. Self-check once before output: 'Is this a record request
  or an advice request?'"

---

## 2. Accreting bans (the meta-example)

- **Mistake:** The agent picked the wrong file to edit.
- **Reflex ban:** "Never edit file X without asking." → Leaks: it then edits file Y
  without asking. You add another ban. The instruction file grows; the gap remains.
- **Category:** Wrong selection.
- **Positive process:** "Before editing any file, state which file and why, and
  confirm it matches the user's named target. Proceed only if they match." (Prevents
  the whole wrong-target class, not just file X.)

---

## 3. Trusting a derived value over the source of truth

- **Mistake:** The agent recomputed a date/figure itself and used the wrong one,
  instead of reading the authoritative record.
- **Reflex ban:** "Don't guess dates." → Leaks: it guesses amounts, IDs, statuses
  next.
- **Category:** Wrong selection (chose a derived value over the source).
- **Positive process:** "When a value exists in an authoritative source, read it from
  there rather than recomputing. If it isn't there, say so instead of inferring."

---

## 4. Pulling in unrelated context

- **Mistake:** A focused request got answered with material dragged in from unrelated
  notes/memory, muddying the answer.
- **Reflex ban:** "Don't cite unrelated memory." → Leaks: it pulls unrelated files,
  or unrelated prior turns, next.
- **Category:** Context blindness.
- **Positive process:** "Use only the source the user named in this request. Pull in
  other context only when this message explicitly references it."

---

## 5. Firefighting instead of building

- **Mistake:** Hit an error and applied a quick patch that made it run, leaving the
  structural cause in place — the error returned in a new form.
- **Reflex ban:** "Don't apply quick fixes." → Leaks: vague, and sometimes a quick fix
  is correct; the agent can't tell which.
- **Category:** Priority failure (skipped diagnosis).
- **Positive process:** "When the same error recurs or a structure smells off, run a
  root-cause pass (deusex Phase 1) before any fix. A patch is allowed only after the
  structural cause is named and the patch is shown not to mask it."

---

## The pattern across all five

Every reflex ban names a *single forbidden act*. Every positive process names a
*gate that opens the right act for the whole category*. The test for a good
conversion: **would it also have prevented the sibling mistakes you haven't made yet?**
If not, you've only blocked one surface of the same root cause.
