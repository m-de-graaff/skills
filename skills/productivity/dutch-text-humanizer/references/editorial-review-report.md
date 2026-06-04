# Editorial review report

Use this template for detector-focused file work. The report is written by the agent after reading the source text. Helper scripts may provide evidence, but the report must include actual editorial judgment.

Save the report next to the output file with the same base name and `.review.md`.

## Template

```markdown
# Editorial review: [document name]

## Verdict

[One short paragraph. Say whether the source reads human, AI-assisted, or heavily model-shaped. Do not claim certainty.]

## Top AI signals

- [Specific signal in this document, not a generic checklist item.]
- [Specific signal in this document.]
- [Specific signal in this document.]

## Concrete facts to preserve

- [Names, dates, numbers, targets, products, clients, teams, constraints.]

## Rewrite strategy

[Explain how the rewrite will change structure, rhythm, specificity, and voice. Mention whether layout is preserved or rebuilt.]

## Final review

[After rewriting, state what changed and which original AI signals were reduced.]

## Residual risk

[Short honest note. Do not promise an external detector result.]
```

## Review rules

- Do not let `profile-humanity` replace the review. It only supplies evidence.
- Quote sparingly. Usually paraphrase the problem.
- Name the exact structural issue: repeated headings, same paragraph role, repeated abstract anchors, too-clean consulting cadence, vague benefits, weak ownership, or low operational detail.
- Keep a fact-preservation checklist. This prevents a deep rewrite from becoming a summary or inventing detail.
- If the final rewrite still has a risk, say so plainly.
