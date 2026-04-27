---
name: pr-walkthrough
description: Manual PR walkthrough workflow for explaining a branch or pull request pedagogically. Use when explicitly invoked for a PR walkthrough or attached by the user.
---

# PR Walkthrough

Use this skill to help the user understand a pull request or branch diff like a senior engineer walking them through it. Optimize for learning first, with review-oriented notes as supporting context.

## Purpose

Explain what the PR does in a pedagogic order:

- Intent and user-visible behavior
- Main changed areas and how they relate
- Key snippets, pseudocode, and flows
- Tradeoffs, assumptions, and choices worth noticing
- Tests and validation paths that matter
- Places where the user can drill down

This is not primarily a code review workflow. Do call out risks, surprising behavior, and review questions, but do not lead with findings unless the user asks for a review.

## Inputs

Default to the checked-out branch compared against `main`.

Before explaining the PR, identify the actual comparison target:

- Use the branch, commit range, PR URL, or base branch named by the user if provided.
- Otherwise compare the checked-out branch against `main`.
- If `main` is unavailable, try `master`.
- If PR metadata is available, prefer the PR's actual base branch.
- Inspect both the final diff and the commit history from base to `HEAD`.

Use the final diff as the source of truth for what changed. Use commit history to infer intent, sequencing, and change groups, but do not structure the walkthrough by commit order unless it tells the clearer story.

## Depth Modes

If the user does not specify depth, use `standard`.

- `quick`: brief orientation, minimal snippets, enough to understand the shape of the PR.
- `standard`: teaching walkthrough with key snippets, pseudocode, tradeoffs, review notes, and pauses.
- `deep`: inspect call sites, tests, edge cases, historical context, alternatives, and ambiguous behavior more thoroughly.

## Discovery Workflow

Do not explain the diff in isolation. For important changed areas, inspect enough surrounding code to teach the change accurately:

- Changed files and final diff
- Commit list from base to `HEAD`
- Relevant callers, callees, interfaces, and tests
- Existing patterns and invariants around the changed code
- Generated, lockfile, or mechanical changes only enough to understand whether they matter

Keep exploration scoped to the PR. Do not turn the walkthrough into a full architecture survey unless the user asks.

## Teaching Order

Reorder the walkthrough to teach the system, not to mirror file order or diff order.

Prefer this order:

- User-facing behavior or product intent
- Entry points and public APIs
- Core domain or data flow
- State, persistence, configuration, or migrations
- Integrations, side effects, async work, or background jobs
- Tests
- Edge cases, tradeoffs, and assumptions

For backend changes, a natural order is request, validation, service logic, persistence, response, tests.

For frontend changes, a natural order is user interaction, component state, data loading or mutation, rendering, tests.

## First Pass Template

Start with a compact map before going deep:

```markdown
## PR Map
- What changed:
- Why it likely changed:
- Main changed areas:
- Suggested walkthrough order:

## Walkthrough
[Teach the PR section by section in dependency order.]

## Key Snippets
[Small curated snippets with explanations and pseudocode where useful.]

## Review Lens
- Tradeoffs:
- Assumptions:
- Behavior changes worth validating:
- Tests that matter:
- Questions for the author:

## Optional Commands
[Commands that could improve understanding, with reasons. Ask before running.]

## Mental Model
- If you remember only three things:
- Good next drill-downs:
```

For large PRs, do not attempt a full walkthrough in one response. Create the PR map, cluster the changes, recommend a path, and pause.

## Large PR Handling

For large diffs, cluster changes by concern before teaching:

- Feature behavior
- API, schema, or contract changes
- Core logic
- UI changes
- Tests
- Generated, dependency, or lockfile changes
- Refactors and file movement

Mark files or clusters as:

- `important`: semantically central to the PR
- `supporting`: useful context, but not the main story
- `mechanical`: generated, formatting, renames, lock churn, or movement
- `ambiguous`: appears mechanical but may alter behavior

Teach semantic changes first. Summarize mechanical changes briefly unless they affect behavior, dependencies, generated APIs, or reproducibility.

## Snippets And Pseudocode

Show small, curated snippets only when they teach something important.

- Prefer the smallest snippet that explains the mechanism.
- Prefer roughly 5-25 lines.
- Avoid quoting unchanged boilerplate.
- Pair each snippet with plain-English explanation.
- Include file references so the user can jump to the source.
- Use pseudocode for complex logic before or after showing code.

Good pseudocode style:

```text
When X happens:
- validate Y
- derive Z
- persist A
- emit B
- return C
```

## Diagrams

Use diagrams only when they clarify structure better than prose. Mermaid is preferred when supported.

Good diagram candidates:

- Request or data flows
- State machines
- Component relationships
- Async or background workflows
- Before/after architecture

Default diagram types:

- `flowchart TD` for process and data flow
- `sequenceDiagram` for interactions over time
- `stateDiagram-v2` for lifecycle or state logic

Do not add diagrams for simple linear changes. If a diagram would mostly repeat the prose, skip it.

Only create a Canvas or other visual artifact when the user asks for one and the harness supports it.

## Observed, Inferred, Unclear

Separate facts from interpretation when it matters:

- `Observed`: directly visible in the diff or surrounding code.
- `Inferred`: likely intent or consequence based on the code.
- `Unclear`: needs author confirmation or runtime validation.

Do not narrate guesses as facts, especially for intent, tradeoffs, and assumptions.

Example:

```text
Observed: retry handling moved from the caller into the service.
Inferred: the intent is probably to centralize failure behavior.
Unclear: whether every caller wants the same retry policy.
```

## Review Lens

Always include a review-oriented section, but keep it secondary to understanding.

Cover:

- Key tradeoffs
- Implicit assumptions
- Behavior changes worth validating
- Tests that matter
- Areas most likely to hide bugs
- Questions to ask the author

If the user asks for a code review, switch to a review-first stance and lead with findings.

## Commands And Validation

Default to read-only exploration. Do not run tests, servers, migrations, package installs, or mutating commands without asking.

When a command would materially improve understanding, offer it with a short reason and ask for confirmation.

Prefer narrow, relevant commands:

- A focused test file or test name
- Typecheck for the touched package
- Build for the affected module
- Generated route or schema inspection
- Snapshot or storybook preview
- CLI output that reveals the changed behavior

Example:

```text
This PR changes the parser boundary. I can run `pnpm test parser.spec.ts` to show which behavior is covered before we inspect edge cases.
```

## Interaction Rules

Pause after each major conceptual section in `standard` and `deep` modes. Offer specific drill-down choices rather than a vague "what next?"

Ask the user questions only when the answer changes the route or depth of the walkthrough. If the question can be answered by inspecting the codebase, inspect the codebase instead.

Good pause:

```text
Want to drill into validation, persistence, tests, or continue to the API response shape?
```

Good route-changing questions:

- Should I treat this as a reviewer walkthrough or onboarding walkthrough?
- Do you care more about the API behavior or the frontend state flow?
- Do you want me to run the focused test before we inspect edge cases?

## Closing Recap

End the first pass with a durable mental model:

- If you remember only three things
- The main runtime path
- The most important assumption or tradeoff
- The best next drill-downs

Keep the recap short and concrete.
