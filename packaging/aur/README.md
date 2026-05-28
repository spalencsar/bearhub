# AUR Packaging

This directory contains starter `PKGBUILD` files for publishing Bearhub on the AUR:

- `bearhub/PKGBUILD`: stable package from tagged releases
- `bearhub-git/PKGBUILD`: rolling package from `main`

Before publishing:

1. Generate `.SRCINFO` with `makepkg --printsrcinfo > .SRCINFO` inside each package directory.
2. Build-test locally with `makepkg -si`.
3. Push each package to its own AUR Git repository (`aur@aur.archlinux.org:bearhub.git` and `aur@aur.archlinux.org:bearhub-git.git`).

Automation:

- You can sync both local AUR clones with one command:
  - `scripts/sync-aur-packaging.sh`
- Optional auto-commit and push:
  - `scripts/sync-aur-packaging.sh --push`
