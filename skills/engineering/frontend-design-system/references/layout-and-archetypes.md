# Layout and Archetypes

## Layout Defaults

- Mobile margin: 16px.
- Tablet margin: 24px-32px.
- Desktop margin: 40px-64px.
- Product app max width: 1440px unless data density requires full width.
- Docs/content max width: 760px-960px.
- Marketing max width: 1120px-1280px.
- Use sidebars for persistent product navigation.
- Use top navigation for marketing/docs or shallow apps.
- Use split panes for developer tools, logs, previews, editors, and admin workflows.

Responsive breakpoints:

```text
Breakpoint | Width  | Behavior
sm         | 640px  | mobile to large mobile
md         | 768px  | tablet / split simple rows
lg         | 1024px | desktop navigation appears
xl         | 1280px | wide dashboard / marketing layout
2xl        | 1536px | dense workspaces only
```

## Shape, Borders, and Elevation

Default radius:

```text
Small controls    | 6px
Buttons / inputs  | 8px
Cards / panels    | 10px-12px
Modals / sheets   | 12px-16px
Tags / pills      | 999px
Tables/data grids | 0px-8px depending container
```

Rules:

- Prefer borders over shadows for standard surfaces.
- Use shadows only for overlays, popovers, modals, drawers, menus, floating panels, and sticky mobile bars.
- Keep cards quieter than the content inside them.
- Do not round every container to 24px.
- Do not use pure black borders in dark mode or near-white invisible borders in light mode.

## Dashboard / Admin App

Use:

- Sidebar navigation.
- Page header with title, description, primary action, and secondary controls.
- Metric cards or compact summary strips.
- Data table/list as the main content.
- Filter/search bar near the data.
- Empty, loading, and error states.

Avoid:

- Marketing hero treatment inside operational views.
- Oversized metric cards that displace the primary task.
- Too many chart colors.

## Developer Tool

Use:

- Command menu.
- Resource-oriented navigation.
- Strong monospace support.
- Logs, code snippets, copy buttons, and status badges.
- Split panes for editor/preview or config/output.

Avoid:

- Decorative AI gradients.
- Fake terminal aesthetics when the task is not terminal-like.
- Low-contrast code blocks.

## SaaS Landing Page

Use:

- Typographic hero.
- Clear product statement.
- Product screenshot/mock UI only when it explains the product.
- Structured feature sections with real content.
- Restrained grid or rule-line system.
- High-contrast CTA.

Avoid:

- Endless generic feature cards.
- Placeholder social proof.
- Abstract neon background as the main identity.

## Consumer Marketplace / Ordering App

Use:

- Search and category navigation.
- Cards/list rows with clear price, availability, status, ETA, and action.
- Sticky cart/checkout affordance on mobile.
- Clear empty/error/offline states.
- Large enough tap targets.

Avoid:

- Dense enterprise UI for consumer browsing.
- Hiding price, delivery time, availability, or action state.
