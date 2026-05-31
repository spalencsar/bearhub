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

## Release Cadence

- `bearhub-git`: continuous
- `bearhub` stable: on validated milestone increments or critical fixes

## Immediate Next Actions

1. Complete M1 gap scan (`bauh` strings still visible in UI and logs).
2. Build M2 issue list from current crash reports and prioritize top 3.
3. Start M3 technical design (import shim + package move order).
