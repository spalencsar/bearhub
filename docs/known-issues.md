# Known Issues and Maintainer Pitfalls

Living document for recurring problems, gaps, and non-obvious workflow traps.  
Update this file when you hit a new issue that cost debugging time.

Last updated: 2026-07-28.

## How to use this file

When you discover or fix a recurring problem, add an entry with:

- **Symptom** — what users/maintainers see
- **Cause** — why it happens
- **Fix** — concrete steps
- **Prevent** — what to do next time (docs, CI, packaging)

AI agents: read this **after** `AGENTS.md` (local) and before invasive changes.

---

## Release and packaging gaps

### Release tag and stable AUR can diverge

| | |
|---|---|
| **Symptom** | GitHub contains a fix, while `yay -S bearhub` still installs an older source tag. |
| **Cause** | GitHub tags and AUR are published separately; changing `main` or creating a tag does not update the AUR clone. |
| **Fix** | Update the stable PKGBUILD tag and checksum, regenerate `.SRCINFO`, then push the local AUR clone. |
| **Prevent** | Complete every step in `packaging/aur/README.md`; verify the source tag shown by AUR after publication. |

### AUR stable builds old tarball

| | |
|---|---|
| **Symptom** | `yay -S bearhub` installs code without latest `main` changes. |
| **Cause** | AUR `bearhub` uses a **tagged** tarball (`0.10.7-bearhub.6`), not `main`. Only `bearhub-git` tracks `main`. |
| **Fix** | Use `bearhub-git` for bleeding edge, or cut a new release tag + PKGBUILD update. |
| **Prevent** | Document in README maintainer section (done). |

### GitHub push does not update AUR

| | |
|---|---|
| **Symptom** | PKGBUILD changed on GitHub; `yay -Ss bearhub` unchanged. |
| **Cause** | AUR is a **separate git repo** (`aur.archlinux.org`). |
| **Fix** | Copy `packaging/aur/*` → local AUR clone → `git push` to AUR (local sync script on maintainer machine). |
| **Prevent** | Never assume `git push origin main` publishes packaging. See `packaging/aur/README.md`. |

---

## AUR / yay / makepkg

### Fresh install fails while an upgrade build succeeds

| | |
|---|---|
| **Symptom** | `yay -S bearhub` fails with `ModuleNotFoundError: No module named 'bauh'` on a clean system, but rebuilding on a maintainer host succeeds. |
| **Cause** | The `0.10.7-bearhub.6` build imported version metadata through `bauh`; an older installed Bearhub supplied that module and masked the missing clean-build path. |
| **Fix** | Use `0.10.7-bearhub.7` or newer, where version metadata is available without a previously installed package. |
| **Prevent** | AUR CI must run a complete `makepkg --cleanbuild` in a fresh Arch container, not only `--verifysource`. |

### SHA256 failed: `bearhub-0.10.7.tar.gz`

| | |
|---|---|
| **Symptom** | `makepkg` / `yay`: `bearhub-0.10.7.tar.gz ... FEHLGESCHLAGEN` |
| **Cause** | Stale cache file with generic name; old `pkgrel` used `bearhub-0.10.7.tar.gz` instead of tag-specific archive. |
| **Fix** | `rm -rf ~/.cache/yay/bearhub`; `yay -Sy`; ensure PKGBUILD uses `bearhub-0.10.7-bearhub.6.tar.gz`. |
| **Prevent** | Always use tag in source filename; bump `pkgrel` when forcing cache refresh. |

### yay shows old `pkgrel` (e.g. `-9` or `-10` while AUR git has `-11`)

| | |
|---|---|
| **Symptom** | `yay -Ss bearhub` lags behind AUR git. |
| **Cause** | Local package DB or yay clone not refreshed; AUR RPC index can trail git briefly. |
| **Fix** | `yay -Sy`; `rm -rf ~/.cache/yay/bearhub`; retry. |
| **Prevent** | After AUR push, wait a few minutes or bump `pkgrel` again if index stuck. |

### AUR SSH: `Permission denied (publickey)`

| | |
|---|---|
| **Symptom** | `git push` to `aur.archlinux.org` fails. |
| **Cause** | Missing key, or `~/.ssh/aur` permissions too open (`0644`). |
| **Fix** | `chmod 600 ~/.ssh/aur`; key registered at https://aur.archlinux.org |
| **Prevent** | `ssh -T aur@aur.archlinux.org` after setup. |

---

## CI and tests

### CI: `ModuleNotFoundError: No module named 'bauh.api'`

| | |
|---|---|
| **Symptom** | GitHub Actions unittest import errors for `bauh.*`. |
| **Cause** | Tests import `bauh.*` but shims missing (partial migration commit) or `pip install -e .` not run. |
| **Fix** | Ensure `bauh/` shims exist; tests use `bearhub.*` for primary imports; CI must `pip install -e .`. |
| **Prevent** | Run full test suite locally before push; 159 tests should pass. |

### Tests pass locally but fail in clean venv

| | |
|---|---|
| **Symptom** | Different results with/without editable install. |
| **Cause** | Running tests without `pip install -e .` — packages not on `PYTHONPATH`. |
| **Fix** | `pip install -e .` then `python -m unittest discover -s tests -p "test_*.py" -v` |
| **Prevent** | Match CI workflow in `.github/workflows/tests.yml`. |

---

## Product / UX (not bugs — known gaps)

### UI still looks like bauh

| | |
|---|---|
| **Symptom** | Bearhub visually identical to upstream. |
| **Cause** | M1 (identity) not done; same PyQt5 themes/layout; `bauh-files` assets/URLs. |
| **Fix** | M1 milestone: branding, screenshots, tray strings, data mirrors. |
| **Prevent** | Do not confuse M3 namespace completion with visual rebrand. |

### Runtime still uses `bauh-files` URLs

| | |
|---|---|
| **Symptom** | Logs/downloads reference `github.com/vinifmor/bauh-files`. |
| **Cause** | Intentional until Bearhub hosts its own datasets (see `0.10.7-bearhub.6` changelog). |
| **Fix** | Future: `bearhub-files` repo or mirrored assets. |
| **Prevent** | Document in M1/M4 before changing URLs. |

---

## Namespace migration (M3)

### Accidental edit under `bauh/` instead of `bearhub/`

| | |
|---|---|
| **Symptom** | Fix works via `import bauh` but `bearhub` path stale. |
| **Cause** | `bauh/` is shim-only; implementation belongs in `bearhub/`. |
| **Fix** | Move logic to `bearhub/`; keep `bauh/` as `from bearhub... import *`. |
| **Prevent** | Grep `bearhub/` for changes; read `NAMESPACE_MIGRATION.md`. |

### Phase D shim removal too early

| | |
|---|---|
| **Symptom** | Breaks users/scripts still using `import bauh`. |
| **Cause** | Removing `bauh/*` before one stable release on shims. |
| **Fix** | Restore shims; wait for tagged stable + AUR cycle. |
| **Prevent** | Follow Phase D checklist in `NAMESPACE_MIGRATION.md`. |

---

## Open runtime issues (M2 — investigate, not fully documented)

| Area | Notes |
|------|--------|
| Uninstall flow | Qt lifecycle / thread teardown crashes reported historically |
| Wayland | Desktop files may force `QT_QPA_PLATFORM=xcb` |
| AppImage + AppImageLauncher | Install crashes possible; documented in README |

Add concrete repro steps here when confirmed on current `main`.

---

## Related docs

- `AGENTS.md` — local AI handoff (gitignored)
- `packaging/aur/README.md` — AUR publish workflow
- `NAMESPACE_MIGRATION.md` — namespace state
- `ROADMAP.md` — M1–M6 milestones
- `CHANGELOG.md` — fixed issues per release
