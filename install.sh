#!/usr/bin/env bash
# Idempotent symlink installer for the Hermes pi skill.
# - Backs up any existing in-Hermes pi directory to a timestamped folder.
# - Replaces the in-Hermes path with a symlink to this checkout via ln -snf.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_SKILLS="${HOME}/.hermes/skills/autonomous-ai-agents"
LINK_PATH="${HERMES_SKILLS}/pi"
BACKUP_ROOT="${HERMES_SKILLS}/.backup"

mkdir -p "${HERMES_SKILLS}"
mkdir -p "${BACKUP_ROOT}"

if [ -L "${LINK_PATH}" ]; then
    current_target="$(readlink "${LINK_PATH}")"
    if [ "${current_target}" = "${SCRIPT_DIR}" ]; then
        echo "[ok] ${LINK_PATH} already symlinks to ${SCRIPT_DIR}"
        exit 0
    fi
    echo "[info] Replacing existing symlink ${LINK_PATH} -> ${current_target}"
elif [ -d "${LINK_PATH}" ]; then
    timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
    backup_dir="${BACKUP_ROOT}/pi-${timestamp}"
    echo "[info] Backing up ${LINK_PATH} to ${backup_dir}"
    mv "${LINK_PATH}" "${backup_dir}"
elif [ -e "${LINK_PATH}" ]; then
    echo "[error] ${LINK_PATH} exists and is neither a symlink nor a directory" >&2
    exit 1
fi

ln -snf "${SCRIPT_DIR}" "${LINK_PATH}"
echo "[ok] Linked ${LINK_PATH} -> ${SCRIPT_DIR}"
