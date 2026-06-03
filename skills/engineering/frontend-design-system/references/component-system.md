# Component System

## Required States

Every component must define relevant states:

```text
default
hover
active / pressed
focus-visible
selected / checked / expanded
disabled
loading
error
success / warning
empty state
```

## Button

Variants:

```text
Primary    | main action       | light: black fill, white text | dark: white fill, black text
Secondary  | alternative       | surface fill, border          | surface fill, border
Tertiary   | low emphasis      | transparent, hover surface    | transparent, hover surface
Accent     | brand highlight   | accent fill                   | accent fill
Danger     | destructive       | danger fill or danger text    | danger fill or danger text
Ghost icon | toolbar action    | transparent, hover surface    | transparent, hover surface
```

Rules:

- Use only one primary action per decision area.
- Loading state must preserve width.
- Icon-only buttons need `aria-label`.
- Danger primary should be rare and usually require confirmation.

## Input / Textarea / Select

Rules:

- Label is required; placeholder is not a label.
- Helper and error text must be associated with the field.
- Focus state must be visible in both modes.
- Validation must not rely only on a red border.
- Inputs should use 8px radius and 12px-16px horizontal padding.

## Card / Panel

Rules:

- Use cards to group related information, not to decorate every line of content.
- Use `surface` + `border` by default.
- Use `surface-2` for nested panels.
- Use `shadow-sm` only when floating or overlapping.
- In dense product UIs, tables/lists may sit directly on the page canvas with borders instead of cards.

## Navigation

Patterns:

- Sidebar: best for apps with persistent sections.
- Top nav: best for marketing, docs, and small apps.
- Command menu: useful for developer tools, dashboards, and power-user flows.
- Breadcrumbs: useful for nested resources and admin views.
- Tabs: switch peer views at the same hierarchy level.

Rules:

- Current navigation state must be clear through more than color.
- Use compact row heights for dense apps, but keep hit areas usable.
- Avoid mixing sidebar, top nav, tabs, and breadcrumbs unless each has a distinct hierarchy role.

## Table / Data Grid

Rules:

- Use body-sm or label-sm for dense tables.
- Use sticky headers only when the table scrolls vertically.
- Provide sort, filter, search, pagination, and empty states when relevant.
- Use row hover subtly; avoid jarring brightness jumps.
- Align numbers and dates consistently.
- Use tabular numerals.
- Use status pills with text labels, not color dots alone.

## Modal / Dialog / Sheet

Rules:

- Trap focus while open.
- Return focus to the trigger after close.
- Use a clear title and concise description.
- Put primary action in the footer or final decision area.
- Use drawers/sheets for mobile or contextual workflows.
- Avoid huge rounded modals unless the brand explicitly needs a softer consumer feel.

## Toast / Notification / Banner

Rules:

- Toasts are transient and should not contain essential-only information.
- Critical errors should persist or provide a details/action path.
- Announce important feedback through live regions.
- Use status color plus text/icon, not color alone.

## Empty State

Rules:

- State what is missing.
- Explain the next action.
- Provide one clear CTA when useful.
- Avoid generic illustrations unless the product has a real illustration system.
- Do not use playful copy in operational tools.

## Code, Logs, Terminal, and Developer Surfaces

Rules:

- Use monospace text with readable contrast.
- Prefer subtle syntax highlighting.
- Use line numbers only when useful.
- Preserve copy actions and keyboard selection.
- Logs should support filtering, severity labels, timestamp alignment, and wrapping/truncation choices.

## Maps, Ordering, Marketplace, and Delivery Flows

Rules:

- Prioritize state, timing, location, and next action.
- Use large touch targets for consumer ordering flows.
- Keep checkout/action bars persistent on mobile when appropriate.
- Separate browse, customize, checkout, tracking, and support states clearly.
- Use status labels such as `Preparing`, `On the way`, `Arriving`, `Delivered`, not just icons.
