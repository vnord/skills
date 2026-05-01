---
name: grug-review
description: >-
  Delete-first review of branch/commit/staged or working diff, repo(s), or
  workspace. Treats lines as carrying cost; YAGNI and KISS; simple bias and
  Ousterhout-style seams (depth, hiding, where complexity lives). Spawns narrow
  exploratory read-only subagents when the diff is insufficient; single
  verbatim grill-me questions only when requirements/coupling stay unclear
  after exploration. Trigger: ruthless, minimal, grug, YAGNI, liability,
  Ousterhout, subtract-code, shave-complexity review.
disable-model-invocation: true
---

# Grug review

Subtract until correctness or stated requirement prevents it; reshaping inside that guardrail must not gratuitously widen surfaces.

Scrutiny: prefer shrinking the scoped change over drive-by refactor. Local boring code beats layers that fail to repay their weight. Flag speculative genericity, unrequested toggles/extra wiring, needless error/policy tax, dormant paths, tighter coupling or wider blast radius. YAGNI without a concrete current ask. Duplicate before wrong abstraction; reject ceremonial structure. Per Ousterhout: complexity belongs behind narrow interfaces that actually hide information; leaking detail through signatures, shapes, or call patterns fails; bury tactical mess inside modules instead of smearing callers; names encode meaning—comments defend non-obvious invariants; dense special cases imply a mistaken model.

Get the diff via attached context when present; otherwise git (`status`, `diff`, logs, merge-base). One clarifying prompt if comparison base unclear—never assume silently. Multiple roots: rinse per checkout; harp on duplication or drifting contracts.

Fan out narrow parallel `explore`-style probes when mental model/call graphs/conventions/outside hunks justify it—not one sprawling agent—and stay read-only unless the user commissioned edits.

**Order**

Semantics and safety first (bad cuts void the mandate to delete); decide what truly must exist; then cross-cutting leaks and misplaced complexity; cosmetic churn only when it hides risk.

Continuous question: fewer types/files/parameters/states/layers?

If rollout, coupling, semantics, etc. survive exploration unanswered, interrogation verbatim:

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

Do **not** use this cadence to stall on discoverable facts (call sites, prior patterns, test coverage). Use it to force explicit trade-offs: scope, compatibility, performance envelope, failure modes, who pays operational cost.

Output stays tight—cite touched files/lines. One-paragraph verdict; subtraction bullets naming what disappears or slips to a later PR; seam notes where depth/hiding/naming/special cases miss the lenses (only actionable observations); unexplored-unknowns condensed to minimal follow-up questions—no fluff praise unless liability clearly dropped.
