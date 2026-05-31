# Namespace Migration (`bauh` -> `bearhub`)

This document defines the technical migration strategy for moving the Python package namespace from `bauh` to `bearhub` safely.

## Current State

- Runtime implementation still lives under `bauh/`.
- Project/package identity is already `bearhub` (metadata, binaries, releases).
- Entry points still target `bauh.*` modules.

## Migration Goals

- Make `bearhub` the canonical Python namespace.
- Keep temporary compatibility for legacy `bauh` imports.
- Avoid breaking AUR/PyPI/runtime while migration is in progress.

## Phase Plan

### Phase A: Introduce target namespace skeleton (current)

- Add `bearhub/` package wrappers that delegate to `bauh/`.
- Keep behavior unchanged.
- Do not switch entry points yet.

### Phase B: Move core modules

Order:
1. `api`, `commons`, `context`
2. `view` / `qt`
3. `gems`
4. CLI + app entry modules

Rules:
- Move one group at a time.
- After each move, keep compatibility imports in `bauh`.
- Run smoke test: start, search, install, uninstall, update.

### Phase C: Flip entry points

- Change project scripts to:
  - `bearhub = bearhub.app:main`
  - `bearhub-tray = bearhub.app:tray`
  - `bearhub-cli = bearhub.cli.app:main`
- Keep compatibility layer for one deprecation window.

### Phase D: Remove legacy compatibility

- Remove `bauh` wrappers only after:
  - one stable release cycle without namespace-related regressions
  - migration completion is documented in changelog

## Compatibility Policy

- During migration, both imports should work:
  - `import bearhub`
  - `import bauh`
- `bearhub` is canonical for new code.
- `bauh` should only be used as temporary compatibility path.

## Verification Checklist

- `python -m py_compile` passes for changed modules.
- GUI starts and basic actions work.
- AUR `bearhub` and `bearhub-git` build/install successfully.
- No user-facing regression in naming/path behavior.
