---
description: Global guidance for all coding agents on this machine
alwaysApply: true
---

# Global Agent Guidance

## Dependency Safety

Assume this machine may use package-manager safety controls such as:

- minimum package release age
- disabled lifecycle or install scripts
- lockfile-enforced workflows

When dependency installation fails:

- consider package policy restrictions before retrying
- do not repeatedly retry the same install command
- do not suggest weakening safety controls unless explicitly asked
- explain the likely policy-related cause and suggest a compliant alternative

For Node ecosystems:

- prefer lockfile-driven workflows
- prefer pinned and fully resolved dependency installs
- prefer CI-safe commands like `npm ci`, `pnpm install --frozen-lockfile`, and `yarn install --immutable` when appropriate
- avoid ad hoc dependency upgrades unless explicitly requested
- avoid unnecessary new dependency additions
- preserve lockfile determinism whenever possible

When proposing fixes:

- prefer solutions that work with package age gates and disabled scripts
- call out when a package is too new and may be blocked by policy
- suggest manual follow-up only when the policy-compliant path is not available

## Task workflow

- On a large task, when a well-defined sub-task is fully implemented, pause so the work can be committed, then request continuation as needed.

## Implementation judgment

- Challenge questionable requests; clarify with context before implementing, especially for questions or options with hidden trade-offs. Push back when a decision has drawbacks the user may not see.
- Prefer explicit behavior over implicit behavior, defaults, and silent fallbacks.
- Keep concerns cleanly separated.
- Prefer referential transparency, composability, and testability. Prefer functional, pure-style approaches where it fits; avoid unnecessary mutation and keep side effects narrow and obvious.

## Code style

- Prefer sentence case.
- Avoid excessive explanatory comments; comment only when something is non-obvious or would be surprising.
- Avoid descriptions that repeat what the code already makes clear.

## Markdown

- Do not use numbered sections in markdown documents (for example, do not structure the document as “1. … 2. …”); use headings and bullets instead.

## Testing

- Prefer a test-driven style when it is practical for the work.
- Avoid mocking; use it only as a last resort, at clear I/O or external boundaries.

## Reviews

- When reviewing code, challenge choices and assumptions, especially implicit ones.

## Git

- Never run destructive or mutating git operations (for example `git commit` or `git push`) without explicit approval. Use git read-only to inspect state.
