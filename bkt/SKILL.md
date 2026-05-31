---
name: bkt
description: Bitbucket CLI for Data Center and Cloud. Use when users need to manage repositories, pull requests, branches, issues, webhooks, or pipelines in Bitbucket. Triggers include "bitbucket", "bkt", "pull request", "PR", "repo list", "branch create", "Bitbucket Data Center", "Bitbucket Cloud", "keyring timeout".
---

# Bitbucket CLI (bkt)

`bkt` is a unified CLI for **Bitbucket Data Center** and **Bitbucket Cloud**. It mirrors `gh` ergonomics and provides structured JSON/YAML output for automation.

Command syntax and flags: [references/commands.md](references/commands.md). Run `bkt <command> --help` when the reference is not enough.

## Dependency check

Before any `bkt` command, verify install:

```bash
bkt --version
```

| Platform    | Command                                                                                               |
| ----------- | ----------------------------------------------------------------------------------------------------- |
| macOS/Linux | `brew install avivsinai/tap/bitbucket-cli`                                                            |
| Windows     | `scoop bucket add avivsinai https://github.com/avivsinai/scoop-bucket && scoop install bitbucket-cli` |
| Go          | `go install github.com/avivsinai/bitbucket-cli/cmd/bkt@latest`                                        |
| Binary      | Download from [GitHub Releases](https://github.com/avivsinai/bitbucket-cli/releases)                  |

Do not proceed until `bkt --version` succeeds.

## Authentication

```bash
bkt auth login https://bitbucket.example.com --web          # DC
bkt auth login https://bitbucket.example.com --username alice --token <PAT>
bkt auth login https://bitbucket.org --kind cloud --web     # Cloud
bkt auth status
```

**Bitbucket Cloud tokens:** "API token with scopes", application **Bitbucket**, scope **Account: Read** (`read:user:bitbucket`); add Repositories / Pull requests / Issues as needed.

## Contexts

```bash
bkt context create dc-prod --host bitbucket.example.com --project ABC --set-active
bkt context create cloud-team --host bitbucket.org --workspace myteam --set-active
bkt context list
bkt context use cloud-team
```

## JSON output traps

List commands return wrapped objects, not bare arrays — `--jq ".[]"` fails.

| Command                  | Root key           |
| ------------------------ | ------------------ |
| `bkt pr list --json`     | `.pull_requests[]` |
| `bkt pr comments --json` | `.comments[]`      |

Use `--json` / `--yaml` on any command. Global overrides: `--context`, `--project`, `--workspace`, `--repo`.

Env: `BKT_CONFIG_DIR`, `BKT_ALLOW_INSECURE_STORE`, `BKT_KEYRING_TIMEOUT` (e.g. `2m`).

Unwrapped endpoints: `bkt api <path> --param ... --json`.

## PR comments: inline by default

When feedback targets specific code, post **inline** on file + line. Reserve general/activity comments for PR-wide remarks. One finding → one inline comment.

| Flag              | Purpose                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------- |
| `--text <msg>`    | Comment body (required)                                                                                     |
| `--file <path>`   | Repo-relative path in the diff; requires `--from-line` and/or `--to-line`                                   |
| `--to-line <n>`   | Line on the **new** side (most common)                                                                      |
| `--from-line <n>` | Line on the **old** side (deletions)                                                                        |
| `--parent <id>`   | Reply in thread                                                                                             |
| `--pending`       | Draft review comment                                                                                        |

```bash
bkt pr comment 42 --file src/auth.ts --to-line 88 --text "..."
bkt pr comment 42 --parent 1001 --text "Fixed in the latest push."
bkt pr comment 42 --text "Overall LGTM; blocking on inline threads."
```

Parallel `bkt pr comment` calls are safe. Line numbers must sit on the diff hunk (read the current file for `--to-line` on Cloud).

## Find open PR for current branch

No `--source` filter. Unwrap `.pull_requests[]`:

```bash
bkt pr list --state OPEN --json \
  | jq --arg b "$(git branch --show-current)" \
    '.pull_requests[] | select(.source.branch.name == $b) | {id, title}'
```

## Resolve comment threads (Cloud)

```bash
bkt api "/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve" --method POST
```

Reopen: same URL, `--method DELETE`. Only inline/diff threads resolve; general comments often `403` — reply with `bkt pr comment <id> --text "..." --parent <comment_id>`.
