# UX v1 — Arch package hub (structure only)

**Status:** draft agreed in principle 2026-08-11 — **design before more chrome code**.  
**Product position:** [`docs/product-position.md`](product-position.md)

## Goal

Make Bearhub **read as an Arch package hub** by clarifying **information architecture**, not by recoloring the old single-table shell.

v1 does **not** require Qt6 or a store redesign.

## Primary jobs (priority order)

1. **See and apply updates** (official + AUR, clearly marked)
2. **Manage installed software** (list, remove, launch when applicable)
3. **Find and install** (search repos/AUR first; other backends secondary)

Tray remains: notify when updates exist → open hub on Updates.

## Three modes (IA)

Replace the mental model “one generic table + many checkboxes” with three explicit modes.
Implementation can still reuse `PackagesTable` and filters at first; the **chrome and defaults** must express the mode.

```text
┌─────────────────────────────────────────────────────────────┐
│  [ Updates | Installed ]     [ search bar …………… ]           │
│  status / progress when working                             │
├─────────────────────────────────────────────────────────────┤
│  filters · primary actions (upgrade when relevant)          │
├─────────────────────────────────────────────────────────────┤
│  package list                                               │
├─────────────────────────────────────────────────────────────┤
│  secondary: themes · settings · about · details console     │
└─────────────────────────────────────────────────────────────┘
```

**Search is not a third mode button** — the search field is always visible; typing/searching enters search results. **Updates** / **Installed** return to the local package list.

### 1. Updates (default when updates exist)

| | |
|--|--|
| **Purpose** | Apply system/AUR updates safely |
| **Default query** | Installed + has update (all relevant types; Arch/AUR emphasized) |
| **Primary action** | Upgrade selected / upgrade all eligible |
| **Chrome** | Count of updates; optional split hint “repo” vs “AUR” later |
| **Avoid** | Full unfiltered system dump as first paint |

### 2. Installed

| | |
|--|--|
| **Purpose** | What is on the machine |
| **Default query** | Installed only |
| **Primary actions** | Uninstall, launch, info, ignore updates |
| **Filters** | Type (Arch/AUR/Flatpak/…), name filter, apps-only optional |
| **Avoid** | Treating “installed” as a hidden checkbox |

### 3. Search (via search bar only)

| | |
|--|--|
| **Purpose** | Find and install |
| **UI** | Always-visible search bar — **no** dedicated mode button |
| **Entry** | User types + submits; results replace the list; list-mode buttons unselected |
| **Exit** | Click **Updates** or **Installed** (reloads installed list) |
| **Primary actions** | Install; open info |
| **Avoid** | Redundant “Search” toggle next to the search field |

## Mapping from current UI (bauh shell)

| Today | UX v1 |
|-------|--------|
| Single window, checkboxes (updates / installed / apps / …) | Mode switch sets those defaults |
| Center search always visible | Search mode owns discovery; other modes keep a lighter filter/name field |
| Upgrade button always in filter row | Primary in Updates; secondary or hidden elsewhere |
| Bottom icon row (suggestions, themes, settings) | Keep settings/about/themes; suggestions fit Search empty state later |
| Suggestions on boot | Optional; prefer Updates-first if `updates > 0` |

No requirement to delete checkboxes in v1 — they can become advanced filters under a mode.

## Visual principles (when implementation restarts)

1. **Structure first** — modes and primary actions before new themes.
2. **One primary action per mode** — amber/honey accent only for that CTA is fine.
3. **Density like a tool** — Pamac / system settings, not marketing landing page.
4. **Mark** — simple flat icon (readable 16–32px); no AI sticker art.
5. **Validate with niri screenshots** before merge (`screenshot-window`).

## Out of scope for v1

- Full visual redesign of every dialog
- Qt6 migration (M6)
- Own store backend / ratings
- Removing multi-backend support

## Acceptance criteria (v1)

- [ ] User can switch **Updates / Installed** without hunting checkboxes *(naive mode bar removed)*
- [x] Search uses the always-visible search bar
- [ ] Cold start with pending updates lands on **Updates** (or equivalent clear path)
- [ ] Arch/AUR remain obvious; Flatpak/AppImage not equally loud in default chrome
- [ ] niri screenshots look intentional
- [x] Existing power features still reachable (details console, custom actions, settings)

## Suggested implementation slices

1. **Docs + product position** — done.
2. **Mode switch chrome** — **reverted (2026-08-11).** Fat checkable `QPushButton`s on top of the bauh shell were not professional UX; removed. Prefer redesigning the **existing** filter/status row (or a real segmented control with design specs) over bolting on a second nav.
3. **Boot routing** — still valid intent (updates-first); implement without a second button bar when revisiting.
4. **Copy / empty states** — when implementation restarts with a design pass.
5. **Light visual pass** — only after structure is designed, not guessed.

### Lesson

Do not ship “hub modes” as bold toggle buttons next to the proven filter checkboxes. That reads as amateur. Either integrate into the existing chrome cleanly or wait for a proper UI design.

## Decision log

| Date | Decision |
|------|----------|
| 2026-08-11 | Product = Arch package hub, not app store |
| 2026-08-11 | UX v1 = Updates \| Installed + search bar (no Search mode button) |
| 2026-08-11 | Dropped redundant Search mode button — search field is always visible |
| 2026-08-11 | Prior visual-refresh layout experiments rejected |
