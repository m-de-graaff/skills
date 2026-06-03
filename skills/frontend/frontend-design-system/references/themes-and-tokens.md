# Themes and Tokens

## Theme Policy

Support light, dark, and system preferences:

```html
<html data-theme="light">
<html data-theme="dark">
<html data-theme="system">
```

Recommended behavior:

- Persist explicit user selection when appropriate.
- Resolve system from `prefers-color-scheme`.
- Always render with semantic CSS variables.
- Test both modes in Storybook, screenshots, and production routes.

Do not:

- Build dark mode by simply inverting light colors.
- Leave dark-mode surfaces under-contrasted.
- Leave light-mode borders too faint.
- Fork component layouts by theme unless layout or imagery truly needs it.
- Define raw hex values inside individual React components.

## Token Architecture

Use four layers:

1. Primitive tokens: raw color, spacing, radius, shadow, duration, easing.
2. Semantic tokens: role-based values such as `--background`, `--surface`, `--foreground`, `--border`, `--accent`.
3. Component tokens: values for buttons, inputs, nav, cards, tables, and overlays.
4. Utility tokens/classes: Tailwind mappings or CSS utility classes that consume semantic tokens.

Component code should consume semantic or component tokens. Raw primitives belong only in token definitions.

## Default CSS Variables

Use this as the default baseline. Adjust only when brand or accessibility testing requires it.

```css
:root,
[data-theme="light"] {
  color-scheme: light;

  --background: #ffffff;
  --background-subtle: #fafafa;
  --background-muted: #f5f5f5;
  --surface: #ffffff;
  --surface-2: #f8f8f8;
  --surface-3: #f1f1f1;
  --surface-overlay: rgba(255, 255, 255, 0.96);

  --foreground: #171717;
  --foreground-secondary: #525252;
  --foreground-tertiary: #737373;
  --foreground-disabled: #a3a3a3;
  --foreground-inverse: #ffffff;

  --border: #e5e5e5;
  --border-subtle: #eeeeee;
  --border-strong: #d4d4d4;
  --border-inverse: #262626;

  --accent: #15803d;
  --accent-hover: #166534;
  --accent-active: #14532d;
  --accent-soft: #ecfdf3;
  --accent-border: #86efac;
  --accent-foreground: #ffffff;
  --accent-text: #047857;

  --success: #15803d;
  --success-soft: #ecfdf3;
  --success-text: #166534;
  --warning: #b45309;
  --warning-soft: #fffbeb;
  --warning-text: #92400e;
  --danger: #dc2626;
  --danger-soft: #fef2f2;
  --danger-text: #b91c1c;
  --info: #2563eb;
  --info-soft: #eff6ff;
  --info-text: #1d4ed8;

  --hover: rgba(0, 0, 0, 0.04);
  --pressed: rgba(0, 0, 0, 0.08);
  --focus: #2563eb;
  --selection: rgba(21, 128, 61, 0.14);

  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 999px;

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 16px 48px rgba(0, 0, 0, 0.12);

  --font-sans: Geist, Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "Geist Mono", "SFMono-Regular", "Roboto Mono", Consolas, "Liberation Mono", monospace;
}

[data-theme="dark"] {
  color-scheme: dark;

  --background: #090909;
  --background-subtle: #0f0f0f;
  --background-muted: #141414;
  --surface: #111111;
  --surface-2: #171717;
  --surface-3: #202020;
  --surface-overlay: rgba(17, 17, 17, 0.96);

  --foreground: #ededed;
  --foreground-secondary: #c7c7c7;
  --foreground-tertiary: #8f8f8f;
  --foreground-disabled: #5f5f5f;
  --foreground-inverse: #090909;

  --border: #262626;
  --border-subtle: #1f1f1f;
  --border-strong: #3a3a3a;
  --border-inverse: #ededed;

  --accent: #3ecf8e;
  --accent-hover: #65d9a6;
  --accent-active: #2eb67d;
  --accent-soft: rgba(62, 207, 142, 0.12);
  --accent-border: rgba(62, 207, 142, 0.36);
  --accent-foreground: #062e1c;
  --accent-text: #6ee7b7;

  --success: #3ecf8e;
  --success-soft: rgba(62, 207, 142, 0.12);
  --success-text: #6ee7b7;
  --warning: #f59e0b;
  --warning-soft: rgba(245, 158, 11, 0.13);
  --warning-text: #fbbf24;
  --danger: #f87171;
  --danger-soft: rgba(248, 113, 113, 0.13);
  --danger-text: #fca5a5;
  --info: #60a5fa;
  --info-soft: rgba(96, 165, 250, 0.13);
  --info-text: #93c5fd;

  --hover: rgba(255, 255, 255, 0.06);
  --pressed: rgba(255, 255, 255, 0.10);
  --focus: #60a5fa;
  --selection: rgba(62, 207, 142, 0.18);

  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 999px;

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.40);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.32);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.32);
  --shadow-lg: 0 16px 48px rgba(0, 0, 0, 0.42);
}
```

## Base Element Setup

```css
html {
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans);
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  min-height: 100vh;
  background: var(--background);
  color: var(--foreground);
  font: 400 14px/1.5 var(--font-sans);
}

*, *::before, *::after {
  box-sizing: border-box;
}

button,
input,
textarea,
select {
  font: inherit;
}

::selection {
  background: var(--selection);
}

:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
```

## Tailwind Token Mapping

Map colors to CSS variables rather than hardcoding palettes in components.

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["selector", '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        "background-subtle": "var(--background-subtle)",
        "background-muted": "var(--background-muted)",
        surface: "var(--surface)",
        "surface-2": "var(--surface-2)",
        "surface-3": "var(--surface-3)",
        foreground: "var(--foreground)",
        "foreground-secondary": "var(--foreground-secondary)",
        "foreground-tertiary": "var(--foreground-tertiary)",
        border: "var(--border)",
        "border-strong": "var(--border-strong)",
        accent: "var(--accent)",
        "accent-soft": "var(--accent-soft)",
        "accent-text": "var(--accent-text)",
        success: "var(--success)",
        warning: "var(--warning)",
        danger: "var(--danger)",
        info: "var(--info)"
      },
      borderRadius: {
        xs: "var(--radius-xs)",
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)"
      },
      fontFamily: {
        sans: "var(--font-sans)",
        mono: "var(--font-mono)"
      },
      boxShadow: {
        xs: "var(--shadow-xs)",
        sm: "var(--shadow-sm)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)"
      }
    }
  }
};

export default config;
```

## Typography

Default font direction:

- Use Geist, Inter, or system UI for product interfaces.
- Use Geist Mono, SF Mono, Roboto Mono, or equivalent for code, IDs, logs, metrics, and technical metadata.
- Do not ship private or proprietary font files unless the project has legal rights.

Recommended scale:

```text
Token       | Size | Line | Weight  | Use
caption     | 12px | 16px | 400/500 | metadata, helper text
label-sm    | 13px | 18px | 500     | table headers, compact labels
body-sm     | 13px | 20px | 400     | dense tables, secondary copy
label       | 14px | 20px | 500     | labels, buttons, tabs
body        | 14px | 22px | 400     | default app copy
body-lg     | 16px | 24px | 400     | forms, modal copy
heading-sm  | 18px | 26px | 600     | section headings
heading     | 24px | 32px | 650/700 | page headings
heading-lg  | 32px | 40px | 700     | top-level pages
display     | 48px | 56px | 700     | rare marketing heroes
```

Rules:

- Most app screens should use 13px-16px text.
- Use 14px body text as the dashboard/product UI default.
- Use tabular numbers for metrics, prices, dates, queue counts, and table columns.
- Avoid more than three type sizes inside one compact component.
- Do not use all caps except for short metadata labels.

## Spacing Tokens

Use a 4px-centered scale:

```text
space-0.5 | 2px  | hairline offsets
space-1   | 4px  | tight icon/text gap
space-1.5 | 6px  | compact vertical rhythm
space-2   | 8px  | standard small gap
space-2.5 | 10px | button/control tuning
space-3   | 12px | common component padding
space-4   | 16px | default gap
space-5   | 20px | medium component padding
space-6   | 24px | section/card padding
space-8   | 32px | major page block gap
space-10  | 40px | large section gap
space-12  | 48px | spacious layouts
space-16  | 64px | hero/page-level separation
space-24  | 96px | rare marketing spacing
```
