#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_BASE="${ROOT_DIR}/packaging/aur"

AUR_BASE_DEFAULT="${HOME}/Projekte/development/current/aur"
AUR_BASE="${AUR_BASE_DEFAULT}"
DO_PUSH=0

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--aur-base <path>] [--push]

Synchronizes PKGBUILD and .SRCINFO from:
  ${SRC_BASE}/{bearhub,bearhub-git}
to local AUR clones:
  <aur-base>/{bearhub,bearhub-git}

Options:
  --aur-base <path>  Local directory containing AUR git clones
                     (default: ${AUR_BASE_DEFAULT})
  --push             Also run git commit + git push in each AUR repo
  -h, --help         Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --aur-base)
      AUR_BASE="$2"
      shift 2
      ;;
    --push)
      DO_PUSH=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

sync_one() {
  local pkg="$1"
  local src_dir="${SRC_BASE}/${pkg}"
  local dst_dir="${AUR_BASE}/${pkg}"

  if [[ ! -d "${src_dir}" ]]; then
    echo "[ERROR] Missing source directory: ${src_dir}" >&2
    exit 1
  fi

  if [[ ! -d "${dst_dir}/.git" ]]; then
    echo "[ERROR] Missing AUR git clone: ${dst_dir}" >&2
    echo "        Clone first: git clone ssh://aur@aur.archlinux.org/${pkg}.git ${dst_dir}" >&2
    exit 1
  fi

  for f in PKGBUILD .SRCINFO; do
    if [[ ! -f "${src_dir}/${f}" ]]; then
      echo "[ERROR] Missing ${src_dir}/${f}" >&2
      exit 1
    fi
    cp -f "${src_dir}/${f}" "${dst_dir}/${f}"
  done
  rm -rf "${dst_dir}/src" "${dst_dir}/pkg"

  if [[ "${DO_PUSH}" -eq 1 ]]; then
    (
      cd "${dst_dir}"
      git add PKGBUILD .SRCINFO
      if git diff --cached --quiet; then
        echo "[${pkg}] No changes to commit."
      else
        git commit -m "Sync packaging from bearhub main repo"
        git push
      fi
    )
  else
    echo "[${pkg}] Synced. Review and push manually in: ${dst_dir}"
  fi
}

sync_one "bearhub"
sync_one "bearhub-git"

echo "Done."
