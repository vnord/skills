---
name: grug-review
description: >-
  Delete-first review of a branch, commit, staged change, working diff, or repo.
  Treats lines as carrying cost; applies YAGNI, KISS, and Ousterhout-style depth
  checks. Use when the user asks for a grug, minimal, YAGNI, or liability review.
disable-model-invocation: true
---

# Grug review

Subtract until correctness or a stated requirement prevents it. Reshaping inside that guardrail must not gratuitously widen surfaces.

Scrutiny:

- Prefer shrinking the scoped change over drive-by refactor.
- Flag speculative genericity, unrequested toggles, needless policy tax, dormant paths, tighter coupling, or wider blast radius.
- Duplicate before wrong abstraction; reject ceremonial structure.
- Prefer narrow interfaces that hide complexity instead of leaking it through signatures, shapes, or call patterns.
- Keep names meaningful; reserve comments for non-obvious invariants.
- Treat dense special cases as evidence of a mistaken model.

Get the diff via attached context when present; otherwise git (`status`, `diff`, logs, merge-base). One clarifying prompt if comparison base unclear—never assume silently. Multiple roots: rinse per checkout; harp on duplication or drifting contracts.

Fan out narrow parallel `explore`-style probes when mental model/call graphs/conventions/outside hunks justify it—not one sprawling agent—and stay read-only unless the user commissioned edits.

**Order**

Semantics and safety first (bad cuts void the mandate to delete); decide what truly must exist; then cross-cutting leaks and misplaced complexity; cosmetic churn only when it hides risk.

Continuous question: fewer types/files/parameters/states/layers?

If rollout, coupling, semantics, or ownership survive exploration unanswered, ask one concrete trade-off question at a time and include the recommended answer. Do not ask about discoverable facts such as call sites, prior patterns, or test coverage.

Output stays tight—cite touched files/lines. One-paragraph verdict; subtraction bullets naming what disappears or slips to a later PR; seam notes where depth/hiding/naming/special cases miss the lenses (only actionable observations); unexplored-unknowns condensed to minimal follow-up questions—no fluff praise unless liability clearly dropped.
