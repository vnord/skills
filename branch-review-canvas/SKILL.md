---
name: branch-review-canvas
description: >-
  Render a supplied branch or commit diff, or the current branch diff against
  main, as a Cursor Canvas that groups changes by reviewer importance,
  separates boilerplate from core logic, and highlights tricky or unexpected
  code. Use when reviewing a branch, commit, local diff, or when the user asks
  for a branch review canvas, diff walkthrough, or change-set overview.
---

# Branch review canvas

Build a canvas that presents the requested diff reorganized for reviewer comprehension, not in file-tree order. For a prose teaching walkthrough, use `pr-walkthrough` instead.

## Prerequisites

Read `~/.cursor/skills-cursor/canvas/SKILL.md` first. Component and hook shapes: `~/.cursor/skills-cursor/canvas/sdk/index.d.ts` and siblings — read, do not guess.

## Comparison base

- Use `@branch`, `@commit`, or another explicit Cursor diff reference when supplied — do not re-discover range with git.
- Else use the checked-out branch against `main`; if absent, try `master`.
- If PR metadata exists, prefer the PR's base branch.
- If the base is still unclear, ask once — do not guess silently.

## Gather the diff

When git is needed (no explicit diff reference):

- `git branch --show-current`, `git status --short --branch`
- `git diff --stat <base>...HEAD` and `git diff --find-renames <base>...HEAD` for committed work
- `git diff --stat` and `git diff --find-renames` for uncommitted edits that belong in the review

If the resolved base ref is missing or diff commands fail, stop and report the blocker. If an explicit reference lacks enough content, ask — do not guess.

## Group changes for comprehension

Not alphabetical or tree order:

- **Core logic**: behavior, algorithms, state, API surface — full diffs with context.
- **Wiring and integration**: routes, DI, config — condensed enough to verify.
- **Boilerplate and mechanical**: imports, renames, generated code — file list + stats unless a hunk matters.

Lead with core logic.

## Distill and call out

- Pseudocode beside dense core hunks (state machines, retries, multi-step transforms) — not for straightforward edits.
- Concrete input walkthrough (old vs new path) only when behavior is hard to predict from the hunk.
- Tags (`Subtle`, `Breaking`, `Race condition`, `Perf`) + one sentence only for genuinely tricky items.

## Tone

Reviewer-facing, terse (one or two sentences): why, cross-file interactions, what the diff hides, whether local edits are in scope.

## Be creative

Sections above are a floor. Pick canvas components (charts, tables, diff views, DAG, cards) that fit this change — refactor vs bugfix vs feature may need different layouts.
