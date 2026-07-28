# AUR Packaging

This directory contains **PKGBUILD templates** for publishing Bearhub on the AUR:

- `bearhub/PKGBUILD`: stable package from **tagged** GitHub releases
- `bearhub-git/PKGBUILD`: rolling package from `main`

**Important:** GitHub and AUR are separate. Updating files here and pushing to GitHub does **not** update the AUR. Publishing requires a **local AUR git clone** and `git push` to `aur.archlinux.org` (see below).

## Current stable snapshot (2026-07-28)

| Field | Value |
|-------|--------|
| `pkgver` | `0.10.7` |
| `pkgrel` | `12` |
| Source tag | `0.10.7-bearhub.7` |
| Source archive | `bearhub-0.10.7-bearhub.7.tar.gz` |

The M3 namespace migration and the clean first-install build fix are released
in `0.10.7-bearhub.7` and published by the stable AUR template.

## Before first publish

1. Generate `.SRCINFO`: `makepkg --printsrcinfo > .SRCINFO` in each package directory.
2. Build-test: `makepkg -si`.
3. Clone AUR repos locally (once):
   ```bash
   git clone ssh://aur@aur.archlinux.org/bearhub.git ~/Projekte/development/current/aur/bearhub
   git clone ssh://aur@aur.archlinux.org/bearhub-git.git ~/Projekte/development/current/aur/bearhub-git
   ```
4. Register SSH public key at https://aur.archlinux.org (key file e.g. `~/.ssh/aur`, mode `600`).

## Publishing workflow (maintainer, local)

1. Edit `packaging/aur/bearhub/PKGBUILD` and `.SRCINFO` in **this** repo; commit and push to **GitHub**.
2. Copy into local AUR clone and push to AUR:
   - **Option A:** local script `scripts/sync-aur-packaging.sh --push` (maintainer machine only — **not** in GitHub repo).
   - **Option B:** manually:
     ```bash
     cp packaging/aur/bearhub/PKGBUILD ~/Projekte/development/current/aur/bearhub/
     cp packaging/aur/bearhub/.SRCINFO ~/Projekte/development/current/aur/bearhub/
     cd ~/Projekte/development/current/aur/bearhub
     git add PKGBUILD .SRCINFO
     git commit -m "updpkgsums: …"
     git push origin master
     ```
3. Users refresh index: `yay -Sy`. If SHA256 fails, clear stale cache: `rm -rf ~/.cache/yay/bearhub`.

## Stable release checklist (`bearhub`)

1. Move `CHANGELOG.md` `[Unreleased]` under a new tag (e.g. `0.10.7-bearhub.7` or `0.10.8`).
2. Commit release changes on `main` and push to GitHub.
3. Create and push the git tag:
   ```bash
   git tag -a 0.10.7-bearhub.7 -m "Release 0.10.7-bearhub.7"
   git push origin main
   git push origin 0.10.7-bearhub.7
   ```
4. Update `bearhub/PKGBUILD`: `_pkgver_tag`, source URL, `sha256sums`; regenerate `.SRCINFO`:
   ```bash
   cd packaging/aur/bearhub
   makepkg --verifysource
   makepkg --printsrcinfo > .SRCINFO
   ```
5. Commit PKGBUILD changes on GitHub `main`.
6. Publish to AUR (local clone + push — step 2 above).
7. Build-test; optional GitHub Release with assets.
