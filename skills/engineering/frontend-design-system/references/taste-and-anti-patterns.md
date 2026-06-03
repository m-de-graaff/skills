# Taste and Anti-Patterns

## Directional Taste Profile

Use these qualities as direction, not as templates to clone.

### Supabase-like Qualities

- Developer/product tooling clarity.
- Clean surfaces with subtle borders.
- Green or emerald accent used sparingly.
- Practical dashboards, forms, tables, logs, empty states, and docs-like patterns.
- Strong support for command/search interactions.
- Components composed from small reusable primitives.

### Vercel / Next.js-like Qualities

- Minimal neutral palette.
- High-contrast text and precise typography.
- Crisp borders, quiet backgrounds, and strong grid discipline.
- Developer-first typography with excellent monospace handling.
- Fast, subtle interactions.
- Marketing sections that are structured and typographic rather than decorative.

### Uber / Base-like Qualities

- Utilitarian product interface.
- Direct action hierarchy.
- Dense but readable spacing.
- Mostly rectilinear forms with controlled radius.
- Strong operational UX for lists, maps, ordering, dispatch, checkout, delivery, status, and marketplace flows.
- Motion used for feedback, not entertainment.

## Anti-Vibe-Code Rules

Avoid:

- Purple/blue/pink gradient blobs as the main visual system.
- Glassmorphism cards over noisy backgrounds.
- Excessive blur, glow, bloom, neon, or cyber effects.
- Oversized rounded cards everywhere.
- Decorative shadows on every surface.
- Random emoji headers or emoji-driven navigation.
- Fake customer logos, fake metrics, fake testimonials, or filler marketing claims.
- Generic hero copy such as "Unlock the power of AI" unless the product truly needs it.
- Unstructured color ramps and one-off hex values in components.
- Centered landing pages where every section has the same rhythm.
- Default shadcn/ui styling left untouched.
- Tailwind class soup without a token system.
- Arbitrary spacing values like 13px, 17px, 19px, 21px, 26px, or 30px unless matching a legacy constraint.
- Motion that delays task completion.
- Components without hover, active, focus, disabled, loading, and error states.

## Design Principles

### Content First

Start with the user's task and data. Every visual treatment must support comprehension, selection, navigation, or confidence.

### Neutral by Default, Accent by Purpose

Use neutral surfaces and strong text hierarchy as the foundation. Use accent color for selection, links, focus, confirmations, progress, and important affordances. Do not use accent color as generic decoration.

### Quiet Surfaces

Use subtle borders, alternating surfaces, and spacing to create structure. Shadows should be rare and reserved for overlays, popovers, modals, floating toolbars, and mobile sheets.

### Dense But Not Cramped

Use tight internal gaps, consistent row heights, readable line heights, and adequate hit areas. Product UIs can be compact without becoming cramped.

### Typography Carries Polish

Use precise type rhythm instead of decorative cards. Strong typography is the main visual signature.

### Components Feel Engineered

Every component must have a predictable API, state model, accessibility behavior, and responsive behavior.

### Semantic Themes

Light and dark mode must use the same semantic token names with different values. Component code should not branch by raw theme color except at the token layer.

## Color Usage

Color hierarchy:

1. Neutral structure: background, surface, border, text.
2. Accent: links, focus, active state, success-adjacent brand affordances.
3. Status: success, warning, danger, info.
4. Data visualization: deliberate palettes with legends, labels, and non-color cues.

Rules:

- Primary CTAs are usually neutral high-contrast buttons: black in light mode, white in dark mode.
- Accent CTAs are acceptable when the product brand or task benefits from it.
- Destructive actions must use danger styling and confirmation when irreversible.
- Warnings must be distinguishable from accent/brand colors.
- Tags and status pills should be low-saturation by default with text that passes contrast.
- Never rely only on color to indicate selected, error, warning, success, or active states.

## Motion

Use motion to clarify state, not to decorate.

```text
Interaction           | Duration  | Notes
Hover/focus color     | 100-150ms | fast feedback
Button press          | 75-100ms  | immediate
Menu/popover enter    | 120-180ms | opacity + 2-4px transform
Menu/popover exit     | 100-140ms | faster exit
Modal/sheet enter     | 180-240ms | scrim + short transform
Modal/sheet exit      | 140-200ms | do not linger
Toast enter/exit      | 160-240ms | avoid blocking flow
Page transition       | 0-220ms   | often unnecessary
```

Reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```
