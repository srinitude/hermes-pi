#!/usr/bin/env bash
# verify-sync — assert sync invariants:
#   1. ~/.hermes/skills/autonomous-ai-agents/pi is a symlink whose realpath
#      resolves to the repo root.
#   2. The repo working tree is clean.
#   3. HEAD == origin/main (after a non-mutating fetch).

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LINK_PATH="${HOME}/.hermes/skills/autonomous-ai-agents/pi"

if [ ! -L "${LINK_PATH}" ]; then
    echo "[error] ${LINK_PATH} is not a symlink" >&2
    exit 1
fi

link_real="$(python3 -c "import os,sys;print(os.path.realpath(sys.argv[1]))" "${LINK_PATH}")"
repo_real="$(python3 -c "import os,sys;print(os.path.realpath(sys.argv[1]))" "${REPO_DIR}")"

if [ "${link_real}" != "${repo_real}" ]; then
    echo "[error] ${LINK_PATH} -> ${link_real}, expected ${repo_real}" >&2
    exit 1
fi

if [ -n "$(git -C "${REPO_DIR}" status --porcelain)" ]; then
    echo "[error] working tree at ${REPO_DIR} is dirty" >&2
    exit 1
fi

git -C "${REPO_DIR}" fetch --quiet origin main || true
head_sha="$(git -C "${REPO_DIR}" rev-parse HEAD)"
remote_sha="$(git -C "${REPO_DIR}" rev-parse origin/main 2>/dev/null || echo '')"

if [ -z "${remote_sha}" ]; then
    echo "[error] origin/main is not known locally; run 'git fetch origin' once" >&2
    exit 1
fi

if [ "${head_sha}" != "${remote_sha}" ]; then
    echo "[error] HEAD ${head_sha} != origin/main ${remote_sha}" >&2
    exit 1
fi

echo "[ok] symlink + clean tree + HEAD == origin/main"
