---
name: split-work-into-commits
description: >-
  Split local changes and current-branch commits into minimal self-contained
  commits that compile, lint, and test independently. Use only when explicitly
  invoked by skill name to rewrite or create commits from the current work.
disable-model-invocation: true
---

# Split work into commits

Split the current pile of work into the smallest coherent commits that each validate independently.

This skill is mutating by design. Use it only when the user explicitly invokes `split-work-into-commits`. Do not treat casual questions like "how would you split this?" as approval to commit or rewrite history.

## Scope

- Include local uncommitted changes: staged, unstaged, and usually untracked files.
- Include existing commits on the current branch since the merge-base with the configured upstream or default branch.
- If the base branch is ambiguous, stop and ask for the base ref.
- Never include unrelated branches or parent-history outside the selected range.
- If rewritten commits already exist on a remote, rewrite locally only. Any `git push --force-with-lease` requires separate explicit approval after the local split succeeds.

## Hard rules

- Create recoverable backups before mutating the index, working tree, or commits.
- Do not discard user work. Avoid destructive commands unless the user explicitly approves the exact operation.
- Stage only named files or hunks. Do not use `git add .` or `git add -A`.
- Every generated commit must compile, lint, and pass relevant tests on its own.
- Keep paired artifacts with the source change that requires them: manifests with lockfiles, migrations with generated clients, snapshots with tests.
- Infer commit message style from recent history. Prefer concise imperative subjects; add bodies only when they explain dependency, ordering, or risk.

## Backup first

Before changing anything:

- Capture branch and upstream state with `git status --short --branch`, `git branch --show-current`, and recent `git log`.
- Create a named backup ref or branch at the original `HEAD`.
- If there is uncommitted work, create a snapshot ref with `git stash create` and `git update-ref`; this must not change the working tree.
- Print the backup refs and exact restore commands before proceeding.

Useful pattern:

```bash
BACKUP_NAME="refs/backup/split-work-into-commits-$(date +%s)"
git update-ref "$BACKUP_NAME" HEAD

SNAPSHOT=$(git stash create "split-work-into-commits snapshot")
if [ -n "$SNAPSHOT" ]; then
  git update-ref "${BACKUP_NAME}-worktree" "$SNAPSHOT"
fi
```

## Plan the split

- Find the base with the current branch's configured upstream when available; otherwise use the repository default branch. If neither is clear, ask.
- Inspect the full selected diff, including untracked files.
- Group changes into the smallest coherent semantic units that can validate independently.
- Order commits by dependency: foundations before consumers, contracts before call sites, tests beside the behavior they verify.
- Use hunk-level staging when needed, but do not split below a coherent story.
- Keep mechanical-only changes separate only when they validate independently and reduce review noise.

## Build each commit

For each planned commit:

- Reset to the selected base or rewrite point using the backup as the recovery anchor.
- Apply and stage only the files or hunks for the next semantic unit.
- Include direct tests, fixtures, generated artifacts, and lockfiles required for that unit to validate.
- Run the narrowest credible compile, lint, and test commands for the touched area.
- Commit only after validation passes.

Discover validation commands from repo instructions, package scripts, CI config, task runners, and recent conventions. If validation commands are ambiguous or unusually expensive, ask before committing.

After all commits are built, run the full compile/lint/test suite once.

## If validation fails

- Treat the first failure as evidence that the candidate commit is missing a dependency or has the wrong boundary.
- Rebalance once by moving the smallest necessary dependent change into the failing commit, then rerun validation.
- If the rebalanced commit still fails, stop. Report the failing commit, the command, the relevant output, and the backup restore commands.
- Do not keep committing after a failed intermediate state.

## Finish

Report:

- The final commit list with subjects and short SHAs.
- Validation commands run per commit and at the end.
- Any files or changes intentionally left uncommitted.
- Whether the rewritten branch differs from its remote, and the exact `git push --force-with-lease` command if the user separately approves pushing.
