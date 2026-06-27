# Namespace Migration (`bauh` -> `bearhub`)

This document defines the technical migration strategy for moving the Python package namespace from `bauh` to `bearhub` safely.

Last updated: 2026-06-27 (Phase D slice: version flip + packaging canonicalization).

## Current State

| Area | Status |
|------|--------|
| Project identity | `bearhub` (PyPI name, binaries, AUR, docs, desktop files) |
| Version source | `bearhub/__init__.py` (`pyproject.toml` → `bearhub.__version__`) |
| Entry points | **Flipped** — `bearhub`, `bearhub-tray`, `bearhub-cli` target `bearhub.*` |
| Runtime implementation | **Native under `bearhub/`** — `api/*`, `commons/*`, `gems/*`, `view/*`, app shell, CLI |
| Legacy `bauh/` tree | Compatibility re-export shims only (+ `bauh/view/resources/` fallback data) |
| `gems/` backends | AppImage, Flatpak, Web, Arch/AUR — all under `bearhub/gems/` |
| Gem loader | Native `bearhub/view/core/gems.py` (dual-root scan + import fallback) |
| Tests | 159 unit tests, all passing (CI: Python 3.11, 3.12) |
| Compatibility shims | `bauh/*` re-exports `bearhub.*`; documented in `CHANGELOG.md` `[Unreleased]` |

### Progress Overview (~95 % of M3 — Phase B complete, Phase D in progress)

```
Phase A  [████████████████████] 100 %  skeleton + wrappers
Phase B  [████████████████████] 100 %  all runtime modules native under `bearhub/` (shims in `bauh/`)
Phase C  [████████████████████] 100 %  entry points on bearhub.*
Phase D  [██████████░░░░░░░░░░]  50 %  version flip done; full shim removal after stable release
```

### Native vs Shim Modules

**Native (implemented in `bearhub/`):**

- App shell: `app_main.py`, `manage.py`, `tray.py`, `context.py`, `stylesheet.py`, `app_args.py`, `app.py`
- CLI: `cli/*`
- `api/*`, `commons/*`, `gems/*`
- `view/util/*`, `view/core/*`, `view/qt/*`
- `view/util/resource.py` prefers `bearhub/view/resources`, falls back to `bauh/view/resources`

**Legacy `bauh/` tree (compatibility shims only):**

- `bauh/api/*`, `bauh/commons/*`, `bauh/gems/*`, `bauh/view/*` — all re-export from `bearhub.*`
- `bauh/app.py`, `bauh/stylesheet.py`, `bauh/context.py` (partial) — thin redirects to `bearhub`

**Still only in `bauh/` (shim-only, pending removal):**

- `bauh/__init__.py`, `bauh/stylesheet.py`, `bauh/app*.py`, `bauh/context.py`, `bauh/manage.py`, `bauh/tray.py`
- `bauh/api/*`, `bauh/commons/*`, `bauh/gems/*`, `bauh/view/*` — re-export shims
- `bauh/view/resources/` — legacy resource fallback (still in `MANIFEST.in`)

**Dead upstream backends (only `__pycache__` left, no `.py` sources):**

- `bauh/gems/debian/`, `bauh/gems/snap/` — skip migration; remove cache dirs during M4 cleanup.

## Migration Goals

- Make `bearhub` the canonical Python namespace.
- Keep temporary compatibility for legacy `bauh` imports.
- Avoid breaking AUR/PyPI/runtime while migration is in progress.
- Complete `gems/` migration before starting M6 (Qt6) to avoid dual refactors.

## Phase Plan

### Phase A: Introduce target namespace skeleton — DONE

- [x] Add `bearhub/` package wrappers that delegate to `bauh/`.
- [x] Add native resource tree at `bearhub/view/resources/`.
- [x] Add desktop integration under `bearhub/desktop/`.
- [x] Keep behavior unchanged during wrapper phase.

### Phase B: Move core modules — DONE

Original order (adjusted based on actual progress):

| Step | Module group | Status | Notes |
|------|-------------|--------|-------|
| B.1 | CLI + app entry | **Done** | `bearhub/app_main.py`, `cli/app_main.py`, `manage.py`, `tray.py` |
| B.2 | `context`, `stylesheet`, `view/core/config`, `view/util/resource` | **Done** | Native implementations |
| B.3 | `api`, `commons` | **Done** | Native under `bearhub/`; `bauh/api` + `bauh/commons` are shims |
| B.4 | `view/util` | **Done** | Native under `bearhub/view/util/`; `bauh/view/util` are shims |
| B.5 | `view/core` | **Done** | Native under `bearhub/view/core/`; `bauh/view/core` are shims |
| B.6 | `view/qt` | **Done** | Native under `bearhub/view/qt/`; `bauh/view/qt` are shims |
| B.7 | `gems/` | **Done** | G.1–G.4 complete |

Rules (unchanged):

- Move one group at a time.
- After each move, keep compatibility imports in `bauh/`.
- Run smoke test after every slice: start, search, install, uninstall, update.
- One release per backend migration slice is acceptable (`0.10.7-bearhub.N`).

### Phase C: Flip entry points — DONE

```toml
# pyproject.toml / setup.py
bearhub = "bearhub.app:main"
bearhub-tray = "bearhub.app:tray"
bearhub-cli = "bearhub.cli.app:main"
```

Legacy redirect: `bauh/app.py` re-exports from `bearhub.app_main`.

Compatibility window: keep `bauh` import path until **Phase D** (target: one stable release after full Phase B).

### Phase D: Remove legacy compatibility — IN PROGRESS

Prerequisites:

- [x] All Phase B groups moved (no `from bauh` in `bearhub/` runtime paths).
- [ ] One stable release cycle (`bearhub` + `bearhub-git`) without namespace regressions.
- [ ] Changelog documents shim removal.

Completed (2026-06-27):

1. [x] `__version__` / `__app_name__` canonical in `bearhub/__init__.py`
2. [x] `bauh/__init__.py` → shim re-exporting from `bearhub`
3. [x] `bauh/stylesheet.py` → shim re-exporting from `bearhub.stylesheet`
4. [x] `pyproject.toml` → `version = {attr = "bearhub.__version__"}`
5. [x] `setup.py` → `APP_PACKAGE = 'bearhub'`, `package_data` only under `bearhub`
6. [x] Tests: `tests/test_namespace_phase_d.py`

Remaining (after one stable release):

1. Delete `bauh/*` compatibility re-export shims (or reduce to minimal stub package).
2. Remove legacy `bauh/view/resources` from `MANIFEST.in` once fallback is no longer needed.
3. Remove `provides=('bauh')` from AUR after deprecation window.
4. Drop `bauh` package from `find_packages` / wheel entirely.

**Target full removal:** earliest `0.10.8` stable (after validated release on current shims).

---

## Gems Migration Plan — DONE (G.1–G.4)

All active gem backends now live under `bearhub/gems/`. The native loader at `bearhub/view/core/gems.py`:

1. Scans `{ROOT_DIR}/gems` where `ROOT_DIR` comes from `bearhub`.
2. Imports `bearhub.gems.{name}.controller` (with `bauh.gems.*` fallback during the shim window).
3. Loads per-gem locale files from `{gem}/resources/locale`.
4. Uses `FORBIDDEN_GEMS_FILE = f'/etc/{__app_name__}/gems.forbidden'` with `bearhub.__app_name__`.

`bauh/view/core/gems.py` is a compatibility shim only. See slice notes below for historical move order.

### Recommended migration order

Migrate smallest / best-tested backends first; leave Arch (largest, most critical) for last.

| PR | Backend | Files | Tests | Risk | Rationale |
|----|---------|-------|-------|------|-----------|
| G.1 | **Loader + AppImage** | 10 + `gems.py` | 4 tests | Low | **Done** — smallest backend; validates loader changes |
| G.2 | **Flatpak** | 10 | 11 tests | Low–medium | **Done** — good test coverage; no pacman coupling |
| G.3 | **Web** | 12 | 14 tests | Medium | **Done** — optional deps (`lxml`, `bs4`); node/nativefier paths |
| G.4 | **Arch/AUR** | 28 | 67 tests | High | **Done** — primary backend; most internal cross-imports |

### Per-slice checklist (repeat for G.1–G.4)

**1. Move source tree**

```bash
git mv bauh/gems/<backend> bearhub/gems/<backend>
```

**2. Update imports inside moved files**

Replace namespace references:

```
bauh.gems.<backend>     →  bearhub.gems.<backend>
bauh.api.*              →  bearhub.api.*      (or keep bauh.* via wrappers during transition)
bauh.commons.*          →  bearhub.commons.*
bauh.view.util.*        →  bearhub.view.util.*
from bauh import ...    →  from bearhub import ...
```

**3. Add compatibility shims in `bauh/gems/<backend>/`**

```python
# bauh/gems/<backend>/__init__.py  (and per-module stubs as needed)
from bearhub.gems.<backend> import *  # noqa: F401,F403
```

**4. Update gem loader (G.1 only, then verify each slice)**

Native `bearhub/view/core/gems.py` must:

- Import `ROOT_DIR` from `bearhub` (not `bauh`).
- Scan `os.path.join(ROOT_DIR, 'gems')`.
- Import `bearhub.gems.{name}.controller` (with fallback to `bauh.gems.{name}.controller` during transition if needed).
- Keep `FORBIDDEN_GEMS_FILE = f'/etc/{__app_name__}/gems.forbidden'` using `bearhub.__app_name__`.

**5. Update packaging metadata**

In `pyproject.toml` and `setup.py`, add/update:

```python
"bearhub": [
    ...
    "gems/*/resources/img/*",
    "gems/*/resources/locale/*",
]
```

**6. Update tests**

Prefer `from bearhub.gems.<backend>...` in test imports. Keep one compatibility test per backend verifying `import bauh.gems.<backend>` still works until Phase D.

**7. Verify**

```bash
python -m unittest discover -s tests -p "test_*.py" -v
bearhub-cli --version
bearhub --help          # offscreen if no display
```

### G.1 detailed steps (first slice) — DONE

Completed 2026-06-27.

**Moved:** `bauh/gems/appimage/` → `bearhub/gems/appimage/` (resources included)

**Rewritten natively:**

- `bearhub/view/core/gems.py` — scans `bearhub/gems/` first, falls back to `bauh/gems/`; imports `bearhub.gems.*.controller` with `bauh.*` fallback
- `bauh/view/core/gems.py` — compatibility shim → `bearhub.view.core.gems`

**Compatibility shims added:**

- `bauh/gems/appimage/*.py` → re-export from `bearhub.gems.appimage.*`
- Extra `bearhub/api/abstract/*` and `bearhub/commons/*` wrappers required by AppImage imports

**Tests:** `tests/gems/appimage/test_util.py` (canonical import), `tests/gems/appimage/test_namespace.py` (compat + loader)

**Result:** AppImage canonical under `bearhub/gems/appimage/`; loader established for subsequent backends.

### G.2 detailed steps (second slice) — DONE

Completed 2026-06-27.

**Moved:** `bauh/gems/flatpak/` → `bearhub/gems/flatpak/` (resources included)

**Compatibility shims:** `bauh/gems/flatpak/*.py` → re-export from `bearhub.gems.flatpak.*`

**Additional wrappers:** `bearhub/api/exception.py`, `bearhub/api/abstract/cache.py`, `bearhub/commons/suggestions.py`, `bearhub/commons/util.py`

**Tests:** flatpak tests switched to `bearhub.*` imports; `tests/gems/flatpak/test_namespace.py` added

**Result:** Flatpak canonical under `bearhub/gems/flatpak/`.

### G.3 detailed steps (third slice) — DONE

Completed 2026-06-27.

**Moved:** `bauh/gems/web/` → `bearhub/gems/web/` (resources included)

**Compatibility shims:** `bauh/gems/web/*.py` → re-export from `bearhub.gems.web.*`

**Additional wrappers:** `bearhub/api/abstract/download.py`, `bearhub/commons/view_utils.py`

**Tests:** web tests switched to `bearhub.*` imports/patch targets; `tests/gems/web/test_namespace.py` added

**Result:** Web canonical under `bearhub/gems/web/`.

### G.4 detailed steps (fourth slice) — DONE

Completed 2026-06-27.

**Moved:** `bauh/gems/arch/` → `bearhub/gems/arch/` (28 Python modules + resources)

**Compatibility shims:** `bauh/gems/arch/*.py` → re-export from `bearhub.gems.arch.*`

**Additional wrappers:** `bearhub/commons/category.py`

**Tests:** all `tests/gems/arch/*` switched to `bearhub.*` imports/patch targets; `tests/gems/arch/test_namespace.py` added

**Result:** All active gem backends canonical under `bearhub/gems/` (Phase B.7 complete).

### B.3/B.4 slice: native `api/` + `commons/` — DONE

Completed 2026-06-27.

**Moved:** `bauh/api/` → `bearhub/api/` (14 modules), `bauh/commons/` → `bearhub/commons/` (15 modules)

**Compatibility shims:** `bauh/api/*.py`, `bauh/commons/*.py` → re-export from `bearhub.*`

**Tests:** `tests/common/*`, `tests/api/abstract/*` switched to `bearhub.*`; `tests/api/test_namespace.py` added

**Result:** `bearhub.api` and `bearhub.commons` are canonical.

### B.4 slice: native `view/util/` — DONE

Completed 2026-06-27.

**Moved:** `bauh/view/util/{cache,disk,logs,translation,util}.py` → `bearhub/view/util/`

**Kept native:** `bearhub/view/util/resource.py` (Bearhub-first resource resolver with `bauh` fallback)

**Compatibility shims:** `bauh/view/util/*.py` → re-export from `bearhub.view.util.*`

**Tests:** `tests/view/util/test_namespace.py` added

**Result:** `bearhub.view.util` is canonical (`resource.py` Bearhub-first with `bauh` fallback).

### B.5 slice: native `view/core/` — DONE

Completed 2026-06-27.

**Moved:** `bauh/view/core/{controller,downloader,settings,suggestions,timeshift,tray_client,update}.py` → `bearhub/view/core/`

**Already native:** `config.py`, `gems.py`

**Compatibility shims:** `bauh/view/core/*.py` → re-export from `bearhub.view.core.*`

**Tests:** `tests/view/core/test_namespace.py` added

**Result:** `bearhub.view.core` is canonical (except `config`/`gems`, already native).

### B.6 slice: native `view/qt/` — DONE

Completed 2026-06-27.

**Moved:** all 18 modules from `bauh/view/qt/` → `bearhub/view/qt/`

**Key import updates:** `bearhub.context`, `bearhub.stylesheet`, `bearhub.view.core/*`, `bearhub.view.util/*`

**Compatibility shims:** `bauh/view/qt/*.py` → re-export from `bearhub.view.qt.*`

**Tests:** `tests/view/qt/test_namespace.py` added

**Result:** Phase B complete — all runtime logic is native under `bearhub/`. Remaining M3 work is Phase D (shim removal after one stable release).

### G.4 Arch-specific notes

Arch has the most cross-module imports (~31 files) and the most tests. Additional care:

- `worker.py` has a lazy import of `ArchManager` — preserve pattern.
- `CUSTOM_MAKEPKG_FILE`, `ARCH_CONFIG_DIR`, pacman integration — smoke-test install/uninstall on a real Arch system or VM.
- Locale files under `gems/arch/resources/locale/` must ship in `package_data`.
- Run full arch test suite: `python -m unittest discover -s tests/gems/arch -v`.

### Phase B completion summary

Phase B (B.1–B.7) is **complete** as of 2026-06-27. All runtime modules are native under `bearhub/`; `bauh/` holds re-export shims only.

**Next (Phase D):** ship one stable release on current shims, then remove `bauh/*` compatibility tree per checklist above. Do not start M6 (Qt6) until M3 is tagged and stable — see `docs/qt6-migration.md`.

---

## Compatibility Policy

During migration, both imports should work:

```python
import bearhub
import bauh          # temporary — deprecated
```

- `bearhub` is canonical for all new code and entry points.
- `bauh` is a compatibility path only; do not add new `bauh` imports.
- `bearhub/__init__.py` currently delegates `__version__` to `bauh` — fix in Phase D.
- User config/cache paths use `__app_name__` (`bearhub`); legacy `bauh` dirs are auto-migrated via `bauh/api/paths.py`.

## Verification Checklist

Run after every migration slice:

- [ ] `python -m unittest discover -s tests -p "test_*.py"` passes
- [ ] `python -m py_compile` on changed modules
- [ ] `bearhub --version` prints expected version
- [ ] `bearhub-cli --help` works
- [ ] GUI smoke test (if display available): start → search → list installed apps
- [ ] Backend-specific smoke test for migrated gem (install/uninstall dry-run or test env)
- [ ] `pip install -e .` succeeds
- [ ] AUR `bearhub` and `bearhub-git` PKGBUILDs build (maintainer check)
- [ ] No new user-facing `bauh` labels in changed UI paths
- [ ] Changelog entry under `[Unreleased]` or next `bearhub.N` tag

## Related Documents

- `ROADMAP.md` — milestone M3 (namespace) and M6 (Qt6, after M3 tag)
- `docs/qt6-migration.md` — Qt6 inventory under `bearhub/view/qt/*` and `bearhub/view/core/*`
- `CHANGELOG.md` — `[Unreleased]` holds full Phase B + partial Phase D notes; tagged slices from `0.10.7-bearhub.4` through `.6`