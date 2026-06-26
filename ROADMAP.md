# Bearhub Roadmap (2026)

This roadmap defines how Bearhub becomes an independent, Arch-first project while keeping release stability.

## Principles

- Keep user-facing stability first.
- Prefer small, reversible changes.
- Ship frequently and document every release-impacting change.
- Keep legacy compatibility only as long as needed.

## Milestones

### M1: Identity Completion (2 weeks)

Scope:
- Remove remaining `bauh` naming from UI text, notifications, tray labels, and docs.
- Ensure links (issues, docs, release checks) point to Bearhub endpoints.
- Verify desktop integration uses Bearhub naming and icon assets.

Definition of Done:
- No user-facing `bauh` labels left in default English UI path.
- README and release notes match actual runtime behavior.
- Basic smoke test passes (start/search/install/uninstall/update).

### M2: Runtime Stability Baseline (2-3 weeks)

Scope:
- Fix known uninstall/Qt lifecycle crash paths.
- Add guardrails around async UI actions and thread teardown.
- Add reproducible bug templates for crash reports.

Definition of Done:
- No known deterministic crash in core uninstall flow.
- Bug reports include enough data to reproduce (backend, package type, logs).
- `bearhub-git` receives at least one stable cycle without critical regressions.

### M3: Namespace Migration (`bauh` -> `bearhub`) (3-5 weeks)

Scope:
- Migrate Python package namespace from `bauh` to `bearhub`.
- Provide temporary import compatibility layer for transition period.
- Move resource paths to Bearhub namespace.

Definition of Done:
- Main entry points import from `bearhub`.
- Compatibility shim exists and is marked for removal date.
- Packaging and tests run successfully with new namespace.

### M4: Backend Governance (2-3 weeks)

Scope:
- Formalize supported backends:
  - Primary: Arch/AUR
  - Secondary: Flatpak, AppImage, Web
- Introduce backend capability flags and cleanup dead code paths.
- Remove unmaintained backend remnants from settings and actions.

Definition of Done:
- Supported backend matrix documented.
- Unsupported backend code is either removed or hard-disabled.
- Settings UI matches actual supported feature set.

### M5: Release and Maintainer Independence (ongoing)

Scope:
- Establish Bearhub release train (`stable` + `-git` cadence).
- Document release checklist and AUR sync workflow.
- Define maintainer responsibilities and review rules.

Definition of Done:
- Repeatable release process documented.
- At least 2 maintainers can publish stable release without ad-hoc steps.
- Changelog quality and release metadata are consistent.

### M6: Qt6 Migration (PyQt5 -> Qt6 bindings) (4-8 weeks)

Context:
- PyQt5 remains viable for short-term maintenance, but Qt5 is in maintenance mode.
- Bearhub already carries Qt5-specific workarounds (for example `QT_QPA_PLATFORM=xcb` on Wayland).
- Qt6 improves Wayland, HiDPI, and long-term distro packaging support on Arch.

Prerequisites:
- M3 namespace migration complete (or near complete) to avoid dual refactors.
- M2 stability baseline in place (thread teardown and uninstall paths understood).

Scope:
- Choose Qt6 binding target: **PySide6** (preferred default: LGPL) or **PyQt6** (if GPL-only strategy is confirmed).
- Migrate `bauh/view/qt/*` and app entry modules to Qt6 APIs.
- Update themes/QSS validation and tray behavior on Wayland.
- Update packaging (AUR deps, AppImage Qt6 bundle, CI GUI smoke checks).

Definition of Done:
- Bearhub starts on Qt6 without requiring `QT_QPA_PLATFORM=xcb` for normal desktop use.
- Tray mode, settings, package table, install/uninstall, and update flows pass smoke tests.
- AUR and documented install paths no longer require `python-pyqt5`.
- No PyQt5 imports left in runtime code paths.

PR Plan (recommended order):

1. **PR-6.1: Qt6 decision + spike** ✅
   - Decision recorded in `docs/qt6-migration.md`: **PySide6** (2026-06-26).
   - Offscreen spike passed on Python 3.14 + PySide6 6.11.1.
   - Exit criteria met for binding choice and local bootstrap feasibility.

2. **PR-6.2: Dependency and packaging switch (dual-stack transition)**
   - Add Qt6 dependency in `pyproject.toml` / AUR while keeping temporary PyQt5 fallback behind a feature flag if needed.
   - Update CI to install Qt6 bindings and run import-level checks.
   - Exit criteria: package installs with Qt6 deps on Arch clean environment.

3. **PR-6.3: Core app shell migration**
   - Migrate `bearhub/app_main.py`, `context.py`, `manage.py`, `tray.py`.
   - Replace deprecated app attributes (`AA_EnableHighDpiScaling`, `AA_UseHighDpiPixmaps`) with Qt6 equivalents.
   - Replace `exec_()` with `exec()` in shared dialog helpers first.
   - Exit criteria: `bearhub --version`, `bearhub --help`, and offscreen window open succeed on Qt6.

4. **PR-6.4: Threading and async UI migration**
   - Migrate `view/qt/thread.py`, `prepare.py`, `systray.py`, `settings.py` signal/slot and `QThread` lifecycle usage.
   - Re-test cancellation paths and worker teardown (M2 crash hotspots).
   - Exit criteria: initialization panel + update check + tray refresh run without thread warnings.

5. **PR-6.5: Main UI migration**
   - Migrate `window.py`, `apps_table.py`, `components.py`, `dialog.py`, `info.py`, `history.py`, `screenshots.py`, `root.py`, `about.py`.
   - Validate custom QSS themes (`light`, `darcula`, `knight`, `sublime`, `default`).
   - Exit criteria: search/filter/install/uninstall/update UX smoke test passes.

6. **PR-6.6: Desktop integration and Wayland validation**
   - Test native Wayland session (remove hard dependency on forced `xcb` where possible).
   - Validate tray icons (`bearhub_tray_*`) and desktop launcher behavior.
   - Exit criteria: no deterministic crash in tray/manage on Wayland during 30-minute session test.

7. **PR-6.7: Distribution hardening + PyQt5 removal**
   - Migrate AppImage builder from pinned PyQt5 to Qt6 runtime layout.
   - Remove PyQt5 from AUR/package metadata and code imports.
   - Update README and maintainer docs with Qt6 runtime requirements.
   - Exit criteria: one stable release published fully on Qt6; PyQt5 marked unsupported.

Rollback strategy:
- Keep PR slices small and releasable; each PR must compile and pass tests.
- If a PR regresses Wayland/tray behavior, revert only that slice and keep dual-stack fallback until fixed.

## Release Cadence

- `bearhub-git`: continuous
- `bearhub` stable: on validated milestone increments or critical fixes

## Immediate Next Actions

1. Close remaining M1 gaps (smoke-test checklist, `NAMESPACE_MIGRATION.md` refresh).
2. Build M2 issue list from current crash reports and prioritize top 3.
3. Continue M3 namespace migration (`gems/` move order + shim removal date).
4. Schedule M6 spike after M3 core move (do not start full Qt6 migration in parallel).
