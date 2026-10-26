---
name: pair
description: Pair-program a finished Rust implementation plan with the user, one small test-first step at a time. The agent supplies validated tests, the API they need, and the surrounding code to read; the user writes the implementation, asks questions, and challenges design decisions along the way. Use when the user wants to implement a Rust change themselves with guidance; not for executing the implementation, walking through existing commits, or reviewing a diff.
metadata:
  opencode/slash: "true"
---

# Test-first Rust pairing

Guide the user through a finished plan as a conversation. Each turn moves one small step and then stops for the user. The user writes and commits the code; the agent supplies tests, context, review, and answers. A reference implementation may exist; it is a guide, not the answer the user must reproduce.

## Before the first step

- Read the plan, repository instructions, relevant code and callers, Git status, and recent commits. Establish the starting revision and what is already done; the Git history is the progress record when resuming.
- Locate the reference implementation if one exists (branch, commit, or patch) and ask for it if the plan mentions one you cannot find. Without one, work out the standard solution for each step yourself before presenting it.
- Check the installed dependency versions before suggesting unfamiliar APIs.
- Give a short overview: the steps as planned, one line each, and where the session starts. Then wait.

## Each step

A step is one behavior: one test commit and one fix commit. Split it across several turns and stop after each:

1. **Test.** Say what behavior is added or fixed and why. Give the complete test, its file and module, the `#[should_panic(expected = "…")]` annotation, any stub it needs, the command, and the expected result. Wait for the user to add it and commit.
2. **Context.** Show the existing code that matters as short excerpts with `path:line`, the signatures the tests require, and suggested std or crate APIs with doc links. Explain Rust concepts this step newly relies on, once, at first use. Ask how the user intends to approach it when the design has a real choice.
3. **Implement.** The user writes the code. On request, give a hint before any code. Show the standard solution only when asked.
4. **Review.** Read the user's actual diff and run the tests and Clippy. Point out correctness problems first, then idiom. Explain why the solution works where it is non-obvious: borrow scopes, conversions, error propagation. Confirm the fix commit removes `#[should_panic]`.

Keep turns short. Do not dump later steps or the full solution ahead of time.

## Questions and challenges

The user may interrupt at any point. Answer the question asked, then return to where the step was.

When the user questions a design decision or proposes an alternative, evaluate it on its merits against the plan's requirements; do not defend the plan or reference by default. Name the concrete consequence either way. If the alternative is better, say so and adapt: adjust the remaining steps, and note where the user's code now diverges from the reference. If it changes the plan's scope or a later commit boundary, confirm with the user before adapting.

## Validation

Do not edit the user's files, stage, or commit unless asked. Validate in an isolated temporary copy of the user's current working tree, so checks reflect their code rather than the reference:

- Before presenting a test: it compiles against the user's code plus the stub and fails at its intended assertion. With the annotation the commit is green; setup failures, `todo!()`, or `unwrap` on missing data must not satisfy the expected message.
- Before showing a standard solution: it passes with the annotation removed, earlier tests still pass, and `cargo fmt` and the repository's Clippy command are clean.

Run the full required checks at the end where feasible. Report what actually ran; never present unexecuted code as tested.

## Tests as the contract

- Test observable behavior. Any correct implementation must pass, including the user's if it differs from the reference; do not assert on helper names, internal structure, or incidental sizes.
- One test per independent expected failure; do not loop over cases where the first panic hides the rest.
- When a test calls an API that does not exist yet, its signature is part of the contract and is shown openly with the test. Supply a compiling stub returning a plausible wrong result so the test reaches its assertion.
- Keep ordinary control tests for behavior that could regress.

Follow [the Rust review guidance](references/rust-correctness.md) for tests, solutions, and reviewing the user's code.

## Style

Match the reader's Rust experience. The reader knows TDD and the `#[should_panic]` workflow; do not explain either. Direct technical prose; no motivational copy or praise for routine work. Explain a construct when it matters, then refer back.
