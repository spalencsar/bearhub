# Qt6 Migration Guide (PR-6.1)

This document defines the technical approach for migrating Bearhub from **PyQt5** to a **Qt6 Python binding**.

Related roadmap milestone: `ROADMAP.md` → **M6: Qt6 Migration**.

## Goals

- Keep Bearhub feature parity during migration (no UI redesign).
- Improve long-term desktop compatibility (Wayland, HiDPI, Arch packaging).
- Remove PyQt5-only workarounds where Qt6 provides stable behavior.
- Land migration in small, reversible PR slices.

## Non-Goals (for M6)

- Rewriting the UI toolkit (GTK, Electron, web UI).
- Visual redesign or UX overhaul.
- Parallel feature development inside migration PRs.

## Prerequisites

- **M3** namespace migration is complete enough that UI modules live under stable `bearhub.*` import paths.
- **M2** thread/uninstall crash paths are documented and reproducible.
- Unit test CI is green (`tests/`, GitHub workflow `tests.yml`).

## Current Qt Footprint (inventory)

Runtime PyQt5 usage is concentrated in:

| Area | Files | Notes |
|---|---|---|
| App entry | `bearhub/app_main.py`, `bearhub/context.py`, `bearhub/manage.py`, `bearhub/tray.py` | app attributes, screen scale env |
| Main window/UI | `bauh/view/qt/window.py`, `apps_table.py`, `components.py`, `dialog.py` | largest migration surface |
| Async/threading | `bauh/view/qt/thread.py`, `prepare.py`, `systray.py`, `settings.py`, `root.py` | `QThread`, `pyqtSignal` |
| Utility/UI helpers | `bauh/view/qt/qt_utils.py`, `about.py`, `info.py`, `history.py`, `screenshots.py` | includes `QDesktopWidget` |
| Settings integration | `bauh/view/core/settings.py` | `QStyleFactory` |
| Misc | `bauh/view/util/util.py` | icon helpers |

Known Qt5-specific patterns in code today:

- `app.exec_()` and dialog `exec_()` calls
- `pyqtSignal` declarations
- `Qt.AA_EnableHighDpiScaling` / `Qt.AA_UseHighDpiPixmaps`
- `QDesktopWidget` screen geometry logic (`qt_utils.py`)
- Forced Wayland workaround in desktop files: `QT_QPA_PLATFORM=xcb`

Packaging/runtime dependencies today:

- Python package: `pyqt5>=5.12` (`requirements.txt`, `pyproject.toml`)
- AUR: `python-pyqt5`
- AppImage builder pins `pyqt5==5.15.10` in `linux_dist/appimage/AppImageBuilder.yml`

## Binding Decision Matrix: PySide6 vs PyQt6

| Criterion | PySide6 | PyQt6 | Notes for Bearhub |
|---|---|---|---|
| Qt version | Qt6 | Qt6 | Equal target platform |
| License | LGPL v3 | GPL v3 / commercial | Bearhub app license is `zlib/libpng` |
| License fit for permissive app | Strong | Weaker unless commercial license purchased | PySide6 is lower compliance risk for distro packaging |
| Arch packaging | `pyside6` | `python-pyqt6` | Arch `[extra]` provides `pyside6` |
| API style | Qt official style (`Signal`, `Slot`) | PyQt style (`pyqtSignal`, `pyqtSlot`) | Mechanical rename/refactor needed either way |
| Documentation/examples | Qt docs + Qt for Python | Riverbank docs | Comparable quality |
| Migration effort from PyQt5 | Medium | Medium-low | PyQt6 is closer syntactically, but not enough to outweigh license fit |
| Long-term maintenance | Qt Company backed | Riverbank | Both active |
| Wayland/tray maturity | Qt6 baseline | Qt6 baseline | Main gain comes from Qt6 itself |

### Recommendation

**Default choice: PySide6**.

Reasoning:

1. Bearhub is permissively licensed (`zlib/libpng`); LGPL binding is a safer default for distribution.
2. Migration effort is dominated by Qt5→Qt6 API changes, not PyQt5→PyQt6 naming alone.
3. Wayland/HiDPI improvements come from Qt6 runtime regardless of binding.

### Decision fallback

Choose **PyQt6** only if maintainers explicitly accept GPL obligations for combined distribution and/or purchase commercial licensing.

Record the final decision in this file before PR-6.2 starts:

```
Decision: PySide6
Date: 2026-06-26
Owner: Bearhub maintainers
Rationale: LGPL fit for zlib-licensed app; Qt6 gains independent of binding choice
```

## Migration Design

### 1) Introduce a thin Qt compatibility layer (short-lived)

Add `bearhub/view/qt/bindings.py` (or similar) exposing:

- signal/slot aliases
- app exec helper
- screen geometry helper
- common enum imports

Purpose: reduce churn while migrating module-by-module. Remove this layer in PR-6.7.

### 2) Mechanical API updates

| PyQt5 / Qt5 pattern | Qt6 target |
|---|---|
| `exec_()` | `exec()` |
| `pyqtSignal` | `Signal` (PySide6) / `pyqtSignal` (PyQt6) |
| `AA_EnableHighDpiScaling`, `AA_UseHighDpiPixmaps` | Qt6 high-DPI env defaults + `QT_SCALE_FACTOR` |
| `QDesktopWidget` | `QScreen` via `QApplication.primaryScreen()` / `screenAt()` |
| enum usage (`Qt.AlignCenter`) | namespaced enums (`Qt.AlignmentFlag.AlignCenter`) where required |

### 3) High-risk functional areas

Prioritize manual validation for:

- tray icon lifecycle and update notifications
- initialization panel thread cancellation (`prepare.py`, `thread.py`)
- uninstall flow teardown (M2 crash history)
- settings window + root password dialog modal behavior
- QSS theme rendering across all bundled themes

## PR Slice Plan (M6)

1. **PR-6.1** (this doc + spike)
2. **PR-6.2** dependency/packaging dual-stack
3. **PR-6.3** app shell migration
4. **PR-6.4** threading/async migration
5. **PR-6.5** main UI migration
6. **PR-6.6** Wayland/tray validation
7. **PR-6.7** remove PyQt5 + distribution hardening

Each PR must:

- compile
- pass unit tests
- include a short manual smoke note in PR description

## PR-6.1 Spike Procedure

Goal: prove Qt6 app boot in <15 minutes on a maintainer machine.

Suggested spike steps:

```bash
python3 -m venv /tmp/bearhub-qt6-spike
/tmp/bearhub-qt6-spike/bin/pip install PySide6  # first install can take several minutes

# offscreen run (must quit explicitly; plain exec() blocks)
QT_QPA_PLATFORM=offscreen /tmp/bearhub-qt6-spike/bin/python -c "
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import QTimer
app = QApplication([])
label = QLabel('Bearhub Qt6 spike')
label.show()
QTimer.singleShot(0, app.quit)
app.exec()
print('spike-ok')
"
```

Spike acceptance criteria:

- chosen Qt6 binding installs cleanly on Arch
- minimal window can open offscreen
- no blocking packaging conflicts with current `python-pyqt5` install path
- maintainer records binding decision in this document

### Spike Result (2026-06-26)

Environment:

- OS: Arch Linux
- Python: `3.14.6`
- Binding installed: `PySide6 6.11.1` (pip wheel in `/tmp/bearhub-qt6-spike`)
- Arch repo package available: `pyside6 6.11.1-1` (`pacman -Ss pyside6`)

Results:

| Check | Result |
|---|---|
| PySide6 install | Pass (`pip install PySide6`) |
| Offscreen window bootstrap | Pass (`spike-ok`) |
| `import bearhub` with PySide6 present in same venv | Pass (metadata import only) |
| Tray availability in offscreen env | Expected false (`QSystemTrayIcon.isSystemTrayAvailable() == False`) |
| Theme icon lookup (`bearhub_tray_default`) in offscreen env | Expected null icon |

Notes:

- Offscreen spike must call `app.quit()` (for example via `QTimer.singleShot`) or the process blocks in `app.exec()`.
- Tray/icon checks are not valid in offscreen mode; validate in PR-6.6 on a real desktop session (X11/Wayland).
- Editable install of Bearhub into the spike venv was not required for PR-6.1 and can be deferred to PR-6.2.

PR-6.1 status: **accepted** (decision + technical spike complete).

## Test Strategy

### Automated

- keep existing unit tests green in every PR
- add import smoke test for Qt binding module once dual-stack starts
- optional CI job later: offscreen `bearhub --version` + window bootstrap

### Manual smoke (required per PR from PR-6.3 onward)

1. `bearhub` starts to manage panel
2. search + filter table
3. install + uninstall small test package
4. update check from tray and panel
5. settings open/close
6. Wayland session test (GNOME/KDE) without forced `xcb` where possible

## Packaging Impact

| Channel | Current | Target |
|---|---|---|
| `pyproject.toml` / `requirements.txt` | `pyqt5` | `PySide6` (or `PyQt6`) |
| AUR `depends` | `python-pyqt5` | `pyside6` (or `python-pyqt6`) |
| AppImage | pinned PyQt5 wheel payload | Qt6 runtime bundle aligned with binding |
| Desktop files | `QT_QPA_PLATFORM=xcb` workaround | remove workaround when Wayland stable |

## Rollback Plan

- Keep PRs small and independently revertible.
- During PR-6.2..PR-6.6, allow temporary dual-stack install docs for maintainers.
- If tray/Wayland regressions appear, revert only the failing PR slice.
- Do not ship stable release with mixed Qt5/Qt6 runtime dependencies.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Tray behavior differs on Wayland | High | dedicated PR-6.6 matrix tests + fallback docs |
| `QThread` teardown regressions | High | migrate threading in isolated PR-6.4 with M2 crash retest |
| QSS theme breakage | Medium | theme snapshot checks for all bundled styles |
| AppImage size growth with Qt6 | Medium | keep module pruning in AppImage `after_bundle` |
| License mismatch (PyQt6 GPL) | Legal/process | default to PySide6 unless explicit maintainer decision |

## Open Questions

- Do we require native Wayland support in first Qt6 stable, or is XWayland acceptable initially?
- Should CI add GUI smoke with `QT_QPA_PLATFORM=offscreen` in M6 or post-M6?
- Do we keep temporary `xcb` launcher fallback for one release cycle after Qt6 cutover?

## Completion Criteria (M6 Done)

- No `PyQt5` imports in runtime modules
- Bearhub stable release published on Qt6 binding
- AUR/AppImage/README no longer list PyQt5
- Wayland smoke test passes without mandatory `QT_QPA_PLATFORM=xcb`
- PyQt5 marked unsupported in changelog and maintainer docs