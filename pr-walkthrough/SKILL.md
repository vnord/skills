---
name: pr-walkthrough
description: Manual PR walkthrough workflow for explaining a branch or pull request pedagogically. Use when explicitly invoked for a PR walkthrough or attached by the user.
---

# PR Walkthrough

Help the user understand a pull request or branch diff like a senior engineer walking them through it. Learning first; review notes secondary. Do not lead with findings unless they ask for a review.

For a **canvas** review layout, use `branch-review-canvas` instead.

## Comparison base

- Use the branch, commit range, PR URL, or base ref the user named.
- Else compare the checked-out branch to `main`; if absent, try `master`.
- If PR metadata exists, prefer the PR's base branch.
- If the base is still unclear, ask once — do not guess silently.
- Treat the final diff as source of truth; use commit history for intent, not walkthrough order unless that tells a clearer story.

## Depth modes

Default `standard` when unspecified.

- `quick`: brief orientation, minimal snippets, no pauses between sections.
- `standard`: teach with key snippets, tradeoffs, review lens, pauses after major sections.
- `deep`: call sites, tests, edge cases, alternatives; same pauses as standard.

## Discovery

For important areas, read enough surrounding code to teach accurately: callers, callees, tests, local patterns. Scope stays on the PR — not a full architecture survey unless asked.

## Teaching order

Teach dependency order, not file or diff order:

- User-facing behavior → entry points / public APIs → core flow → persistence / config / migrations → integrations / async → tests → edge cases and tradeoffs.

Backend: request → validation → service → persistence → response → tests. Frontend: interaction → state → data → render → tests.

## First pass

Open with a short **PR map** (what / why / main areas / suggested order). Then teach section by section. Include a secondary **review lens** (tradeoffs, assumptions, tests that matter, author questions).

Large PRs: map and cluster only in the first response; recommend a path and pause — do not walk everything at once.

Cluster tags: `important`, `supporting`, `mechanical`, `ambiguous`. Teach semantic changes first; summarize mechanical churn unless it affects behavior or reproducibility.

## Snippets and claims

- Snippets only when they teach; roughly 5–25 lines; pair with plain English and file refs; pseudocode for dense logic when helpful.
- Label non-obvious intent as **Observed** (in diff/code), **Inferred** (likely intent), or **Unclear** (needs author/runtime) — do not state guesses as facts.
- Mermaid only when structure is clearer than prose; skip for simple linear changes. Canvas only when the user asks and the harness supports it.

## Commands

Read-only by default. Offer narrow commands (focused test, package typecheck, module build) with a reason; ask before running anything mutating or expensive.

## Interaction

In `standard` and `deep`, pause after major sections with specific drill-down choices. Ask the user only when the answer changes route or depth; otherwise inspect the codebase.

Close the first pass with three memorable points, the main runtime path, and the best next drill-downs.
