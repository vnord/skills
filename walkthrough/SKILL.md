---
name: walkthrough
description: Walk interactively through every commit on a branch (usually compared to master) to fully understand it — each commit's motivation, what the code is doing, and line-by-line Rust explanation where it matters. A teaching conversation, not a review; for a terse reviewer-facing canvas use branch-review-canvas, for implementing a plan use tutorial.
metadata:
  opencode/slash: "true"
  opencode/autoinvoke: "false"
---

# Rust branch walkthrough

Walk the user through a branch one commit at a time in conversation: why each commit exists, what changed, and what the interesting lines do. The user reads and asks questions; you explain. Stay read-only: never check out, reset, stash, commit, or otherwise change repository state.

## Resolve the branch and base

- If the user named a branch or range, use it. Otherwise use the current branch (`git branch --show-current`).
- Base defaults to `master`; use `main` only if no `master` exists. Prefer a base the user or a PR supplies. If the base is still ambiguous, ask once — do not guess silently.
- Compare with merge-base semantics: commit list `git log --reverse --oneline <base>..<branch>`, per-commit detail `git show <rev>`, whole-branch diff `git diff <base>...<branch>`.
- If the commit list is empty (already merged, wrong base, detached HEAD), report what you found and ask how to proceed instead of inventing a range.
- Note uncommitted changes if present. Walk committed work only by default, and say explicitly that the working tree is excluded unless the user asks to include it.

## Map before teaching

Before the first commit, read enough to explain motivation rather than guess at it:

- Repository guidance and README for domain context.
- The relevant files at the base revision (`git show <base>:<path>`) so the "before" state is concrete.
- Each commit's message, stat, and diff. Trace moved or rewritten code with `git log --follow` and `git blame` when a line's history explains the change.
- Treat commit messages as claims, not facts. Verify each message's promise against the actual diff; when a commit does more, less, or something else than the message says, say so.

Open the walkthrough with an overview: the commit list with a one-line purpose for each, grouped into themes where natural, and how the commits build on each other. If it helps calibrate depth, ask whether this is the user's own work returning after time away or someone else's branch. Confirm the plan before diving in.

## Walk one commit at a time

Oldest first. For each commit:

1. **Motivation.** The concrete problem the commit solves and why it belongs at this point in the sequence. Distinguish what the message says, what the code shows, and what you infer. If the motivation is genuinely unknowable from the repository, say so and ask — the user may know.
2. **What changed.** Files and symbols, bounded to what matters. Cover boilerplate (imports, formatting, generated code) with a one-line note, not a walkthrough.
3. **The code**, line by line where it matters. Quote exact lines with file and symbol locations. Explain the lines that carry behavior: state transitions, error paths, invariants, tricky conditions, concurrency, allocation. Do not narrate obvious punctuation, familiar setup, or every import.
4. **Checkpoint.** Pause. Invite questions, answer them from the code, then move on when the user is satisfied.

Group only trivially related commits (a rename split across two commits, for example) and say why you grouped them. Never dump the whole branch in one message.

## Explain the Rust

- Match the user's Rust experience. Explain a construct when it first matters — ownership and where a borrow ends, lifetimes, trait bounds, `Option`/`Result` flow, conversions, `unsafe`, locks and atomics, async — then refer back instead of repeating it.
- Explain both the construct and its job in this code: why a value must be owned rather than borrowed on this path, why one error is propagated and another logged, what invariant an assert protects.
- Verify language and API claims against the code and the dependency versions actually in use; read the dependency source when behavior is not obvious. Do not guess the semantics of an unfamiliar API.
- Show the relevant before-state from git history rather than describing it from memory.

## Honest limits

- Never invent motivation, authorial intent, or results you did not observe. Label inference as inference.
- Running a branch's tests at an old revision requires checking that revision out. Do not do it silently; offer a separate worktree only if the user wants verification.
- If a diff is too large to explain usefully, summarize its structure first, go deep on the parts that carry behavior, and say what you skimmed.
- If the branch references an issue or PR you cannot read, say those notes are missing rather than reconstructing them.
