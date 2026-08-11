# Bearhub product position

**Status:** agreed 2026-08-11  
**Branch context:** post visual-refresh fail; layout chrome reverted.

## One-liner

> **Bearhub** is a graphical **package hub for Arch Linux**: manage official and AUR packages, apply updates safely, and optionally handle Flatpak and AppImage.

## What we are

| We are | We are not |
|--------|------------|
| Arch-first **package manager GUI** / software **hub** | A full **app store** (Featured, ratings, curated catalog server) |
| Frontend over **pacman + AUR** (and secondary backends) | Owner of package indexes or a proprietary store API |
| Focused on **updates, installed software, search/install** | Multi-distro shopping experience |

## Why this position

1. **Matches the codebase** — table + actions + multi-gem controllers, not storefront data.
2. **Matches the fork** — maintenance and Arch compatibility, not content curation.
3. **Clear competitor gap** — many GUIs are generic; Bearhub can feel **Arch/AUR-native**.
4. **Shipable** — UX work sharpens workflows; a store pivot would be a rewrite.

## Backends (governance preview)

| Priority | Backend | UI treatment |
|----------|---------|--------------|
| Primary | Arch repos + AUR | Default filters, updates prominence, copy/docs |
| Secondary | Flatpak, AppImage, Web | Available, not equally marketed on home/chrome |
| Removed / dead | Debian, Snap | Do not re-surface |

## Non-goals (near term)

- Store-style home with marketing carousels
- Own suggestion CDN / review system (keep existing suggestion hooks only if useful)
- Parallel Qt6 + full redesign + store IA in one effort

## Related docs

- UX structure: [`docs/ux-v1.md`](ux-v1.md)
- Roadmap M1 / later UX: [`ROADMAP.md`](../ROADMAP.md)
