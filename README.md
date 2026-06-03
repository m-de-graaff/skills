<p>
  <a href="https://skills.sh/m-de-graaff/skills">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skills-repo-dark_2x.png">
      <source media="(prefers-color-scheme: light)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png">
      <img alt="Skills" src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="369">
    </picture>
  </a>
</p>

# Skills For Real Engineers

[![skills.sh](https://skills.sh/b/m-de-graaff/skills)](https://skills.sh/m-de-graaff/skills)

Agent skills for real engineering work.

This repo is where I keep small, composable skills that help coding agents work with more discipline: clarifying intent, designing from real constraints, debugging deliberately, writing better tests, improving architecture, and handing work off cleanly.

The goal is not to hand control of the whole process to an agent. The goal is to give the agent sharper workflows that are easy to inspect, adapt, and combine.

The first skill is [`database-schema-designer`](./skills/engineering/database-schema-designer/SKILL.md), a workload-first database design workflow for SQL and NoSQL systems.

## Quickstart (30-second setup)

Run the skills.sh installer:

```bash
npx skills@latest add m-de-graaff/skills
```

Pick the skills you want, and choose which coding agents you want to install them on.

Then invoke the skill you need from your agent. For database design work, use `/database-schema-designer`.

## Why These Skills Exist

Coding agents are useful, but they fail in predictable ways:

- They misunderstand the goal.
- They produce too much vague output.
- They make changes without tight feedback loops.
- They add complexity faster than they remove it.
- They apply generic patterns where the workload calls for a more specific design.

Skills are a lightweight way to correct those failure modes. Each skill should do one job well, document the workflow clearly, and leave enough room for the engineer to stay in control.

For example, `database-schema-designer` makes the agent start with access patterns, volume, latency targets, retention, and operational constraints before it proposes tables, collections, indexes, partitions, or migrations.

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
README.md
```

## Reference

### Engineering

- **[database-schema-designer](./skills/engineering/database-schema-designer/SKILL.md)** - Design workload-aware SQL and NoSQL schemas with indexes, migrations, ERDs, hot query examples, and performance rationale.

### Productivity

No productivity skills added yet.

### Misc

No miscellaneous skills added yet.
