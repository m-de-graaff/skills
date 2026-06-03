# Accessibility and QA

## Accessibility Requirements

Every design must satisfy:

- Text contrast meets WCAG AA for intended text size.
- Focus state is visible in light and dark mode.
- Every interactive element is keyboard reachable.
- Modal/dialog focus is trapped and restored.
- Inputs have programmatic labels.
- Help and error messages are associated with fields.
- Icon-only buttons have accessible names.
- Status, selected, error, warning, and success states do not rely only on color.
- Reduced motion is respected.
- Content remains usable at 200% zoom.
- Mobile touch targets remain usable.

## Review Checklist

### Visual Quality

- Does it look like a real product screen rather than a concept mockup?
- Is the primary action obvious?
- Is the accent color used sparingly and intentionally?
- Are surfaces structured with borders/spacing before shadows?
- Are radii controlled and consistent?
- Are spacing values tokenized?
- Are typography sizes and weights consistent?
- Are both light and dark modes intentionally designed?

### Anti-Template Quality

- No generic gradient blob hero.
- No glass cards over noisy backgrounds.
- No fake logos/testimonials/metrics unless supplied.
- No arbitrary colors or one-off Tailwind values.
- No default component-library look left untouched.
- No excessive emojis, glows, or decorative motion.

### Component Quality

- Every component has default, hover, active, focus, disabled, and loading/error states where relevant.
- Tables, forms, modals, nav, and empty states are specified.
- Density is appropriate for the user and task.
- Responsive behavior is specified.
- Keyboard and screen-reader behavior is covered.

### Implementation Quality

- CSS variables are used for theme values.
- Tailwind maps to tokens.
- Raw hex values live only in token files.
- Theme provider is hydration-safe.
- Storybook or screenshot tests cover light and dark modes.
- Reduced-motion behavior exists.

## Response Style

- Be specific and decisive.
- Name the design direction and explain why it fits the product.
- Give concrete layout and component details.
- Include tokens or code when useful.
- Do not over-explain obvious UI concepts.
- Do not output generic inspiration-board language without implementation details.
- Prefer precise language such as "12px horizontal padding, 1px border, 8px radius" over vague language such as "modern card styling".

## Default Design Brief Template

Use this internally when the user gives a vague request:

```text
Product type: dashboard / app / landing / marketplace / docs
Audience: developer / operator / consumer / admin
Primary task: what users do most
Density: compact / standard / spacious
Theme: light + dark + system
Accent: emerald green unless provided
Navigation: sidebar / top nav / tabs / command menu
Main surface: table / list / cards / editor / map / form
Must avoid: generic AI gradients, glassmorphism, excessive rounded cards, fake content
```

## Final Delivery Expectations

A strong frontend design answer should leave the user with one of:

- A complete UI direction with tokens and component specs.
- A production-ready React/Next.js component or page scaffold.
- A clean redesign plan with before/after rationale.
- A design-system module that can be pasted into a project.
- A QA checklist that prevents regressions into generic or inaccessible UI.

## Validator Usage

When the design spec is saved to Markdown:

```bash
python skills/engineering/frontend-design-system/scripts/validate_frontend_design.py path/to/design.md
```

Or from stdin:

```bash
type design.md | python skills/engineering/frontend-design-system/scripts/validate_frontend_design.py -
```

The validator checks structure and quality signals. It does not replace visual QA in a browser, screenshot tests, or accessibility tooling.
