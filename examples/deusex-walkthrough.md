# /deusex walkthrough: a recurring "works on my machine" bug

A worked example of diagnosing to the structural cause instead of patching, with a
falsifiable recurrence proof.

---

**Symptom report:** "The nightly job sometimes writes a half-finished file. Adding a
retry didn't fix it — it just fails less often."

## Phase 1 — Diagnosis

- **D1. Symptom** — The output file is occasionally truncated; downstream readers get
  partial data.
- **D2. Direct cause** — The job writes directly to `output.json`; if it crashes
  mid-write, the file is left partial.
- **D2-M. Workflow decomposition** —
  - A. fetch data ✅
  - B. transform ✅
  - C. write to `output.json` ❌ (non-atomic write is the failure point)
  - D. downstream read ⚠️ (reads whatever C left, including partial files)
- **D3. Structural cause (why ×5)** — Why partial? Because the writer streams into the
  final path. Why does that matter? Because readers point at the same path with no
  signal of "done." Why no signal? Because "writing" and "published" are the same
  state. **Root: there is no atomic boundary between in-progress and complete.**
- **D4. Recurrence condition** — Any crash, OOM, or kill *during* the write to the
  final path, at any time a reader happens to look.
- **D5. Complexity contribution** — The retry added control-flow complexity while
  leaving the race intact, so the system got *more* complex and no safer.

## Phase 2 — Redesign

- **Before:** `job → write stream → output.json ← reader`  (writer and reader share
  the live path)
- **After:** `job → write to output.json.tmp → fsync → atomic rename → output.json ← reader`
- **Elegance check:** one atomic `rename()` replaces the retry loop entirely.
- **Side-effect check:** readers always see either the old complete file or the new
  complete file, never a partial one; the `.tmp` is on the same filesystem so rename
  is atomic.
- **Entropy check:** the retry loop is deleted. Net complexity goes *down*.

## Phase 3 — Recurrence-impossibility proof

> D4 said this recurs on any crash during the write to the final path. In the After
> architecture, the job only ever writes to `output.json.tmp`; `output.json` is
> updated solely by an atomic `rename()`, which either completes or doesn't. A crash
> mid-write can only leave a stale `.tmp`, never a partial `output.json`. The path
> that produced a truncated published file is therefore unreachable, regardless of
> timing.

Contrast with the retry patch, which could only reduce the *probability* of D4, never
eliminate it — the tell that it was a patch, not a redesign.
