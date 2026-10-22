---
name: tutorial
description: Turn a Rust implementation plan and the current repository into an illustrated tutorial with correct, idiomatic, validated Rust, explanations matched to the reader, and commit checkpoints. Use when the user wants to implement a Rust change themselves from a tutorial; not for executing the implementation or reviewing an existing diff.
metadata:
  opencode/slash: "true"
---

# Rust implementation tutorials

Create an editable tutorial and offline HTML from the user's plan. The user writes and commits the implementation unless they explicitly ask otherwise. Correctness and idiomatic Rust take precedence over shorter or easier-looking snippets.

## Ground the tutorial

- Read the plan, repository instructions, current code, callers, Git status, and recent commits. Establish the starting revision, completed work, remaining behavior, and relevant tests.
- Preserve scope and commit boundaries. Do not restart completed steps or introduce unrelated refactors. Ask only about consequential choices the plan and repository do not resolve.
- Match the reader's Rust experience. Explain ownership, borrowing, lifetimes, trait bounds, patterns, conversions, error propagation, and iterators where the examples use them. Explain each concept when it matters, then refer back rather than repeating it.
- Inspect the installed dependency version before using an unfamiliar API. Follow repository Rust guidance and applicable Rust skills when available.

## Make the Rust correct before teaching it

- Review the connected code, not only the proposed diff. Check invariants, compatibility, error paths, malformed input, and ownership across the whole operation. Follow [the Rust review guidance](references/rust-correctness.md).
- Prefer existing types, helpers, error conventions, and standard library facilities. Avoid abstractions introduced only to demonstrate a Rust feature. Use the least code that fully preserves the required behavior.
- Prefer borrowing over unnecessary cloning, but make an owned copy when mutation or lifetime requirements justify it and explain that cost. Use narrow visibility and only the trait bounds actually needed.
- Use checked conversions and explicit validation at input boundaries. A cast or invariant-based `expect` needs a reason established by the surrounding code. Propagate recoverable failures; do not turn malformed input into panics or silently discard meaningful data.
- Do not teach an unidiomatic shortcut because it is easier to explain, disable a useful lint to accommodate the example, or weaken a meaningful test just to obtain green checks. When a legitimate test assumption changes, replace it with a stronger behavior-level check and explain why.

## Validate the commit sequence

- Apply proposed edits in an isolated temporary copy preserving relevant repository configuration and fixtures. Do not edit the user's Rust files, stage changes, or create commits while preparing the tutorial.
- Follow the plan's TDD convention. For this user's `#[should_panic]` workflow, observe the unannotated test fail at its intended assertion, add a unique expected message for the test commit, and remove the attribute in the immediately following fix commit. Setup failures must not satisfy that expected panic. Expected-panic tests return `()`.
- Keep each documented intermediate commit buildable and green under its intended annotations. Add ordinary controls for behavior that could regress. Do not group independent expected failures in a loop where the first panic hides later cases.
- Test observable behavior and meaningful invariants. Avoid round-trip-only tests when reader and writer bugs could conceal each other, implementation-mirroring assertions, and arbitrary byte sizes for structurally equivalent data.
- Run formatting, relevant tests, and Clippy at each meaningful stage, then the repository's required full checks where feasible. A clean Clippy run is not proof of semantic correctness; review the invariants too. Record actual checks and limits, never unexecuted snippets as tested.
- Export snippets and optional complete stage diffs from the validated states. The document builder must never apply patches, execute Rust, or alter Git history.

## Write the walkthrough

For each commit, explain the concrete reason for the change, give exact file/symbol locations, complete edits or bounded replacements, explain interesting Rust lines, and provide commands, expected results, and a commit checkpoint. Clearly label fragments that show only a signature or changed line.

Assume the reader already understands TDD and the expected-panic workflow. Apply that workflow and show the necessary annotations, commands, and results, but do not add a TDD primer, rhythm/lifecycle diagram, or motivational explanation of test-first development unless requested. Time should go into the Rust and the implementation's reasoning.

Explain both the Rust construct and its job here: why collecting entries ends a borrow before a mutable read, why a conversion is safe, or why a test isolates the actual bug. Explain buffer ownership, error versus panic behavior, and any non-obvious allocation. Do not narrate obvious punctuation or repeatedly explain familiar setup lines.

Illustrate actual structures and behavior: data layouts, flow, byte offsets, borrow lifetimes, state transitions, or before/after representations. Prefer accessible SVG with captions and a textual explanation. No decorative images are needed.

Use direct technical prose. No slogans, motivational copy, invented branding, fake quotes, claims of craftsmanship, or promotional headings. Avoid lines such as “Your code. Your commits.”, “One behavior at a time.”, “A small fix. A precise format.”, and “Six commits. Three precise fixes.” Name the implementation and the next action. Do not invent reading times or say “carefully tested” instead of stating what ran.

## Build and check the output

Read [the authoring and build reference](references/authoring.md) when producing files. Included Python/page assets provide offline navigation, code copying without line numbers, checkpoints, themes, print styling, and inline SVGs without package installation. Do not carry over an earlier project's subject, code, diagrams, slogans, or test results.

Initialize a new directory:

```bash
python3 <skill-directory>/scripts/init_tutorial.py <output-directory> \
  --title 'Concrete Rust implementation title' \
  --project 'Project name' \
  --description 'The behavior and scope covered.' \
  --baseline '<starting revision>'
```

Honor a requested destination; otherwise use a named directory under the repository's `docs/`. The initializer refuses nonempty directories and creates document scaffolding only. Write the tutorial, validated snippets, and diagrams before delivery.

Rebuild with `python3 <output-directory>/build.py`, then run `python3 <skill-directory>/scripts/check_tutorial.py <output-directory>` for link, ID, code-fidelity, and runtime-asset checks. Also verify accessible illustrations. Inspect desktop/narrow layouts and controls when a browser is available; state a preview limitation rather than claiming an unavailable visual check.

Deliver HTML and expanded Markdown links, the rebuild command, and actual validation results and limits. Do not publish, install/link the skill elsewhere, or change ignore rules unless requested.
