#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
source_file="${repo_root}/AGENTS.md"

link_file() {
  local target_file="$1"

  if [[ -L "${target_file}" && "$(readlink "${target_file}")" == "${source_file}" ]]; then
    printf 'Already linked: %s -> %s\n' "${target_file}" "${source_file}"
    return
  fi

  if [[ -e "${target_file}" || -L "${target_file}" ]]; then
    printf 'Refusing to replace existing path: %s\n' "${target_file}" >&2
    printf 'Move or remove it first, then rerun this script.\n' >&2
    return 1
  fi

  ln -s "${source_file}" "${target_file}"
  printf 'Linked: %s -> %s\n' "${target_file}" "${source_file}"
}

if [[ ! -f "${source_file}" ]]; then
  printf 'Missing source file: %s\n' "${source_file}" >&2
  exit 1
fi

mkdir -p "${HOME}/.claude"

link_file "${HOME}/AGENTS.md"
link_file "${HOME}/.claude/CLAUDE.md"
