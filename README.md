# Skills For Real Engineers

Agent skills for real engineering work.

This repo is where I keep small, composable skills that help coding agents work with more discipline: clarifying intent, designing from real constraints, debugging deliberately, writing better tests, improving architecture, and handing work off cleanly.

The goal is not to hand control of the whole process to an agent. The goal is to give the agent sharper workflows that are easy to inspect, adapt, and combine.

The current skills cover workload-first database design and disciplined frontend design systems.

## Quickstart (30-second setup)

Run the skills.sh installer:

```bash
npx skills@latest add m-de-graaff/skills
```

Pick the skills you want, and choose which coding agents you want to install them on.

Then invoke the skill you need from your agent:

- `/database-schema-designer` for workload-aware SQL and NoSQL schema design.
- `/frontend-design-system` for polished product UI, design tokens, component states, and light/dark themes.

## Why These Skills Exist

Coding agents are useful, but they fail in predictable ways:

- They misunderstand the goal.
- They produce too much vague output.
- They make changes without tight feedback loops.
- They add complexity faster than they remove it.
- They apply generic patterns where the workload calls for a more specific design.

Skills are a lightweight way to correct those failure modes. Each skill should do one job well, document the workflow clearly, and leave enough room for the engineer to stay in control.

For example, `database-schema-designer` makes the agent start with access patterns, volume, latency targets, retention, and operational constraints before it proposes tables, collections, indexes, partitions, or migrations. `frontend-design-system` makes the agent specify product direction, layout, tokens, component states, accessibility, and implementation details instead of producing generic UI decoration.

## Repository Structure

Current structure:

```text
skills/
  engineering/
    database-schema-designer/
      SKILL.md
      agents/
        openai.yaml
      references/
        migrations-and-operations.md
        nosql.md
        output-quality.md
        sql.md
        workload-first-design.md
      scripts/
        validate_schema_design.py
    frontend-design-system/
      SKILL.md
      agents/
        openai.yaml
      references/
        accessibility-and-qa.md
        component-system.md
        implementation-patterns.md
        layout-and-archetypes.md
        taste-and-anti-patterns.md
        themes-and-tokens.md
      scripts/
        validate_frontend_design.py
README.md
```

## Reference

### Engineering

- **[database-schema-designer](./skills/engineering/database-schema-designer/SKILL.md)** - Design workload-aware SQL and NoSQL schemas with indexes, migrations, ERDs, hot query examples, and performance rationale.
- **[frontend-design-system](./skills/engineering/frontend-design-system/SKILL.md)** - Design polished product UIs with semantic tokens, light/dark themes, responsive layouts, component states, and implementation guidance.

### Productivity

No productivity skills added yet.

### Misc

No miscellaneous skills added yet.
