---
name: frontend-design-system
description: Design product UIs and systems: layouts, tokens, components, dashboards, states, accessibility, QA.
---

# Frontend Design System

Create refined, production-grade frontend designs for modern web applications. Aim for precise, useful, technical, mature product UI. Use Supabase, Vercel/Next.js, and Uber/Base as directional taste references only; do not copy their brand assets, logos, exact layouts, screenshots, proprietary font files, or trade dress.

## Core Mandate

Optimize every design for:

1. Clear task flow: the user immediately understands what can be done.
2. Strong hierarchy: primary action, navigation, status, and state are obvious.
3. Production realism: the screen looks like a shipped product, not a concept shot.
4. Light/dark parity: both themes are intentionally designed.
5. Implementation readiness: tokens, spacing, states, accessibility, and responsive behavior are specified.
6. Restraint: no decorative noise, fake depth, random gradients, or generic AI visual tropes.

## First-Pass Decisions

Before designing, identify or infer:

- Product type: dashboard, SaaS app, marketplace, consumer app, developer tool, admin panel, docs site, landing page, or mobile web app.
- Primary user: developer, operator, admin, consumer, creator, analyst, or internal team.
- Main actions: create, search, filter, order, deploy, monitor, configure, pay, invite, approve, review, or export.
- Data density: compact, standard, or spacious.
- Brand accent: default emerald/green unless the user provides a brand color.
- Tech stack: default React/Next.js + Tailwind CSS + CSS variables + Radix/shadcn-compatible primitives unless specified otherwise.
- Theme behavior: default light, dark, and system modes with manual override.

If details are missing, proceed with reasonable defaults and state assumptions briefly.

## Standard Output

For design requests, respond in this order unless the user asks otherwise:

1. Design direction: one concise paragraph describing the intended feel.
2. Information architecture: regions, hierarchy, and navigation model.
3. Layout specification: grid, spacing, breakpoints, responsive behavior.
4. Visual system: color, typography, radius, border, elevation, motion.
5. Component specifications: component anatomy and state matrix.
6. Light/dark theme tokens: CSS variables or token table.
7. Implementation guidance: React/Next.js/Tailwind/shadcn notes when useful.
8. Accessibility and QA checklist: contrast, focus, keyboard, screen reader, reduced motion.

For code requests, produce implementation-ready code that consumes tokens rather than hardcoding raw colors and style values inside components.

## Reference Loading

Load only the references needed for the current task:

- `references/taste-and-anti-patterns.md`: taste direction, anti-vibe-code rules, visual principles, color usage, motion.
- `references/themes-and-tokens.md`: light/dark/system policy, CSS variables, base element setup, Tailwind token mapping, typography, spacing.
- `references/layout-and-archetypes.md`: responsive layout, page archetypes, dashboards, developer tools, landing pages, marketplaces.
- `references/component-system.md`: component requirements, buttons, inputs, cards, nav, tables, dialogs, toasts, empty states, logs, marketplace flows.
- `references/implementation-patterns.md`: theme provider, button baseline, product page shell, code implementation defaults.
- `references/accessibility-and-qa.md`: accessibility requirements, review checklist, response style, design brief template, validator usage.

## Quality Bar

- Use semantic tokens and component tokens; raw primitives live only in token definitions.
- Specify hover, active, focus-visible, disabled, loading, error, selected, and empty states where relevant.
- Prefer borders, spacing, and typography before shadows.
- Use motion for state feedback only, and respect reduced motion.
- Avoid fake logos, testimonials, metrics, decorative gradients, glassmorphism, excessive blur/glow, emoji-driven navigation, arbitrary Tailwind values, and untouched default component-library styling.
- Before finalizing a design artifact, run `scripts/validate_frontend_design.py` on the Markdown when practical.
