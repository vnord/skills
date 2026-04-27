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

## Implementation judgment

- Challenge questionable requests with context before implementing, especially when they are phrased as questions or carry hidden trade-offs.
- Prefer explicit code over implicit behavior.
- Keep concerns cleanly separated.
- Prefer referential transparency, purity, composability, and testability.

## Code style

- Prefer sentence case.
- Avoid excessive explanatory comments; comment only when something is non-obvious or would be surprising.
- Avoid descriptions that repeat what the code already makes clear.

## Reviews

- When reviewing code, challenge choices and assumptions, especially implicit ones.

## Git

- Never invoke git commands that mutate repository state unless explicitly approved.
- Use git for observing current state.
