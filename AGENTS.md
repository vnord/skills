---
description: Global guidance for all coding agents on this machine
alwaysApply: true
---

# Global Agent Guidance

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial, bounded tasks, prefer acting over interrogating.

## Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- Challenge questionable requests; clarify with context before implementing, especially for questions or options with hidden trade-offs.
- Prefer explicit behavior over implicit behavior, defaults, and silent fallbacks.
- Keep concerns cleanly separated.
- When reviewing code, challenge choices and assumptions — especially implicit ones.
- Prefer functional, pure-style approaches only when they reduce total complexity for this task; avoid unnecessary mutation and keep side effects narrow and obvious.

## Simplicity first

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If your draft is much longer than the task warrants, rewrite it before presenting — without expanding scope into surrounding code.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## Surgical changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports, variables, and functions that your changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

## Goal-driven execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → write tests for invalid inputs, then make them pass
- "Fix the bug" → write a test that reproduces it, then make it pass
- "Refactor X" → ensure tests pass before and after

Prefer test-driven style when practical. Avoid mocking except at clear I/O or external boundaries.

For multi-step tasks, state a brief plan with a verification step for each stage.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Task workflow

- Commit verified sub-tasks as part of normal workflow — do not wait for an explicit "commit" request.
- On large tasks, commit regularly rather than accumulating one large diff at the end.
- Aim for small, self-contained commits: one logical change that is easy to review, revert, or cherry-pick on its own.
- Each commit must leave the tree green and correct; do not commit broken, failing, or knowingly incomplete work.
- When a well-defined sub-task is fully implemented and verified, commit it, then continue with the next sub-task.

## Code style

- Prefer sentence case.
- Avoid excessive explanatory comments; comment only when something is non-obvious or would be surprising.
- Avoid descriptions that repeat what the code already makes clear.

## Markdown

- Do not use numbered sections in markdown documents (for example, do not structure the document as "1. … 2. …"); use headings and bullets instead.

## Local project guidance

- When working in a repository, after reading the normal project instructions, check for an `AGENTS.local.md` file at the repository root. If it exists, read it too; it is developer-specific, git-ignored guidance for that project.
- Treat `AGENTS.local.md` as local-only: do not stage, commit, push, print secrets from it, or assume it exists for other contributors.
