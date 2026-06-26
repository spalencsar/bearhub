# AUR Packaging

This directory contains starter `PKGBUILD` files for publishing Bearhub on the AUR:

- `bearhub/PKGBUILD`: stable package from tagged releases
- `bearhub-git/PKGBUILD`: rolling package from `main`

Before publishing:

1. Generate `.SRCINFO` with `makepkg --printsrcinfo > .SRCINFO` inside each package directory.
2. Build-test locally with `makepkg -si`.
3. Push each package to its own AUR Git repository (`aur@aur.archlinux.org:bearhub.git` and `aur@aur.archlinux.org:bearhub-git.git`).

## Stable release checklist (`bearhub`)

1. Update `CHANGELOG.md` and packaging paths for the new tag (e.g. `0.10.7-bearhub.6`).
2. Commit all release changes on `main`.
3. Create and push the git tag:
   ```bash
   git tag -a 0.10.7-bearhub.6 -m "Release 0.10.7-bearhub.6"
   git push origin main
   git push origin 0.10.7-bearhub.6
   ```
4. Refresh tarball checksum in `bearhub/PKGBUILD`:
   ```bash
   cd packaging/aur/bearhub
   makepkg -g >> PKGBUILD  # or updpkgsums after source URL is reachable
   makepkg --printsrcinfo > .SRCINFO
   ```
5. Sync to local AUR clones:
   ```bash
   scripts/sync-aur-packaging.sh
   ```
6. Build-test both AUR packages, then publish AUR commits.
7. Optional: create GitHub release from tag `0.10.7-bearhub.6`.
