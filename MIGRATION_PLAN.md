# Bearhub Migration Plan

This plan translates the roadmap into concrete engineering tasks with sequencing and acceptance criteria.

## Phase 0: Inventory and Risk Mapping

Tasks:
- Enumerate remaining `bauh` references:
  - Python imports
  - resource paths
  - UI strings
  - desktop entries
  - log prefixes
- Classify each reference as:
  - user-facing
  - internal-only
  - compatibility-critical

Acceptance:
- Single tracking list with owner and status for each category.

---

## Phase 1: User-Facing Decoupling

Tasks:
- Replace user-visible `bauh` names with `Bearhub`.
- Normalize status/notification/error message prefixes.
- Validate desktop launcher and tray naming.

Acceptance:
- No user-facing `bauh` in default UI flow.
- Docs and runtime naming are aligned.

---

## Phase 2: Namespace Transition Architecture

Tasks:
- Define target namespace: `bearhub`.
- Create temporary compatibility package:
  - `bauh` imports forward to `bearhub`.
- Define migration order:
  1. core modules
  2. qt/view modules
  3. gem backends
  4. tests

Acceptance:
- Design note committed with:
  - shim scope
  - deprecation window
  - removal criteria

---

## Phase 3: Incremental Code Migration

Tasks:
- Move modules in small batches.
- Update imports and resource path lookups per batch.
- Keep compatibility imports passing until final cut.
- Run smoke tests after each batch:
  - app start
  - package search
  - install
  - uninstall
  - update

Acceptance:
- Main application runs from `bearhub` namespace.
- Legacy imports still function during transition.

---

## Phase 4: Packaging and Distribution Alignment

Tasks:
- Update `pyproject`/entry points to final namespace.
- Validate AUR (`bearhub`, `bearhub-git`) install paths and desktop files.
- Ensure release tags and checksums reflect migrated structure.

Acceptance:
- Stable and `-git` packages build/install successfully.
- No stale paths in PKGBUILD or runtime scripts.

---

## Phase 5: Compatibility Removal

Tasks:
- Announce shim deprecation in changelog.
- Remove `bauh` compatibility layer after deprecation window.
- Run full regression smoke test and release candidate.

Acceptance:
- Codebase is fully `bearhub` namespace.
- No required runtime dependency on legacy `bauh` package structure.

---

## Tracking Template

Use this minimal template per task:

- `Task`: short description
- `Owner`: maintainer
- `Status`: todo / in-progress / blocked / done
- `Risk`: low / medium / high
- `Verification`: command or scenario used to validate

---

## First Technical Slice (recommended now)

1. Add `NAMESPACE_MIGRATION.md` with exact module move order.
2. Implement compatibility shim skeleton (`bauh` -> `bearhub` forwarding).
3. Migrate one low-risk module group and validate with smoke test.
