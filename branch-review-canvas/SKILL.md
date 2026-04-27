---

## name: branch-review-canvas
description: >-
  Render a supplied branch or commit diff, or the current branch diff against
  main, as a Cursor Canvas that groups changes by reviewer importance,
  separates boilerplate from core logic, and highlights tricky or unexpected
  code. Use when reviewing a branch, commit, local diff, or when the user asks
  for a branch review canvas, diff walkthrough, or change-set overview.

# Branch review canvas

Build a canvas that presents the requested diff reorganized for reviewer comprehension, not in file-tree order.

## Prerequisites

Read `~/.cursor/skills-cursor/canvas/SKILL.md` first. It contains the generation policy, design guidance, slop rules, self-check, and file-path conventions you must follow. The full component and hook surface is declared in `~/.cursor/skills-cursor/canvas/sdk/index.d.ts` and its sibling `.d.ts` files. Read them to discover exact exports and prop shapes rather than guessing.

## Gather the diff

If the user supplied an explicit Cursor context reference, such as `@branch` or `@commit`, treat that reference as the diff under review. Use the already-supplied context instead of running local git discovery commands just to infer a branch or commit range.

If the user did not supply an explicit diff reference, assume they want to review the current branch against `main`. Use local git commands only:

- `git branch --show-current` to identify the branch under review.
- `git status --short --branch` to capture branch state and uncommitted changes.
- `git diff --stat main...HEAD` to collect changed files and overall additions/deletions.
- `git diff --find-renames main...HEAD` to collect every committed hunk since the branch diverged from `main`.
- `git diff --stat` and `git diff --find-renames` when the working tree has uncommitted changes that should appear in the canvas as local edits.

If `main` is unavailable or the diff command fails, stop and report the exact blocker. Do not switch to another base branch unless the user explicitly asks. If an explicit Cursor reference is incomplete or does not include enough diff content to build the canvas, ask the user for the missing diff context instead of guessing.

## Group changes for comprehension

Do not present files in alphabetical or tree order. Reorganize into sections ordered by reviewer value:

- **Core logic**: New behavior, algorithm changes, state transitions, and API surface changes. Show full diffs with surrounding context.
- **Wiring and integration**: Route registration, dependency injection, and config plumbing that connects the core logic. Condense enough to confirm correctness.
- **Boilerplate and mechanical**: Import reordering, renames, generated code, formatting, and type re-exports. Summarize as a list of file names and stats. Avoid inline diffs unless a hunk is specifically relevant.

Lead with core logic. The reviewer's attention is freshest at the top.

## Distill complex logic into pseudocode

When a core change involves dense or intricate logic, add a short pseudocode summary next to the diff. Use this for deeply nested conditions, state machines, retry or backoff flows, and multi-step transformations.

The pseudocode should strip away language syntax, error handling, and boilerplate to expose the essential algorithm or control flow in a few lines. Straightforward changes do not need a pseudocode mirror.

## Trace tricky logic on a concrete example

When a hunk changes behavior in a way that is hard to predict from reading it, pick a concrete input and walk it through the old and new paths side by side. Highlight the step where they diverge and the observable outcome.

Use this for genuinely surprising behavior changes, such as reordered effects, new short-circuits, or altered edge cases. Do not trace every core hunk.

## Call attention to tricky things

When a hunk contains something surprising, risky, or easy to miss, visually separate it from the surrounding diff and pair it with a short tag, such as "Subtle", "Breaking", "Race condition", or "Perf". Add a one-sentence explanation so the reviewer sees the concern and the code together.

Reserve these callouts for genuinely tricky items. Overuse destroys signal.

## Tone and content

Write reviewer-facing commentary, not a changelog. Focus on:

- Why something changed, not just what changed.
- Interactions between files, such as a validator in one file being invoked by a route in another.
- Anything the diff alone does not make obvious.
- Whether local uncommitted edits are part of the review or separate from the committed branch diff.

Keep commentary terse. One or two sentences per note.

## Be creative

The sections above are a floor, not a ceiling. The goal is the fastest possible path for the reviewer to understand this specific change, so look at the diff in front of you and ask what representation would actually help.

A tiny state diagram, a before/after call graph, a table of input-to-output pairs, a timeline of commits, a confidence annotation per file, or a single large callout with everything else collapsed may fit better than a uniform walkthrough.

The canvas SDK has charts, tables, diff views, DAG layout, cards, stats, interactive state, and more. Reach for whichever components best serve the change at hand. A review of a refactor looks different from a review of a bug fix or a new feature. Let the canvas reflect that.