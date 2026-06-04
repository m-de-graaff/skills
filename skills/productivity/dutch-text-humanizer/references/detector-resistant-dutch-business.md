# Detector-resistant Dutch business rewriting

Use this reference when the user reports GPTZero, AI detector feedback, or a human review saying the Dutch text still feels AI-written.

The goal is not to trick a detector. The goal is to remove the writing habits that make a document read like a model output: a neat consulting skeleton, repeated abstract anchors, low specificity, and paragraphs that all carry the same rhythm.

## Failure pattern

Dutch strategy documents often fail after a light "humanizer" pass because the rewrite only swaps words:

- The same headings remain in the same order.
- Every section is still one clean heading plus one balanced paragraph.
- Abstract terms keep returning: `platform`, `structureel rendement`, `propositie`, `regie`, `schaalbaar`, `terugkerende diensten`.
- The text explains ambitions without showing decisions, constraints, risks, ownership, or operational consequences.
- The voice is too polished: no sentence feels like it came from a board memo written under time pressure.

If those signals remain, the document still looks AI-assisted even when the obvious AI vocabulary is gone.

## Deep rewrite moves

- Preserve facts, numbers, names, and intent. Do not preserve the old structure by default.
- Merge sections that repeat the same strategic point.
- Split dense paragraphs when they contain separate decisions.
- Cut generic claims unless the source gives a mechanism.
- Replace repeated anchor phrases with the actual mechanism: who does what, which team owns it, which market is affected, what changes commercially, what risk is accepted.
- Use the source's concrete anchors early: dates, targets, companies, teams, products, operating units, returns, FTE, contract cycles.
- Let paragraph length vary. A Dutch executive note can have one-line paragraphs next to longer explanation.
- Allow sober friction. A human strategy note can admit that discipline, governance, partner selection, or reinvestment choices are hard.

## What not to do

- Do not add anecdotes, quotes, customers, timelines, or risks that are not in the source.
- Do not pretend there is evidence when the source only gives an ambition.
- Do not turn every heading into a sentence with the same grammar.
- Do not replace every repeated business term with a synonym. Consistency is sometimes necessary. Reduce repetition by changing structure, not by cycling synonyms.
- Do not make the document casual when the audience is management, investors, or board-level stakeholders.

## Rewrite shape for short strategy DOCX files

For a short board or strategy document, prefer this shape over the original AI-style section chain:

1. Title and date.
2. One direct executive thesis.
3. A few compact sections with uneven length:
   - what changes commercially
   - where VCS/COPE will focus
   - how operations and technology support the model
   - what the financial rule is
4. A short decision list with concrete choices.

Use headings only when they help the reader navigate. A heading followed by one generic paragraph is usually weaker than a tighter combined section.

## Final audit

Before writing the final file, check:

- Are there still many repeated abstract anchors?
- Does every paragraph have the same role and length?
- Could a reader identify what VCS/COPE will actually do differently?
- Are KPN, Eurofiber, SOC, NOC, VCS Observation, VCS Multimedia, the 15% return target, the one-third reinvestment rule, the €25 million ambition, and the 100 FTE point preserved when they appeared in the source?
- Are all em dashes, en dashes, chatbot phrases, and unsupported specifics gone?
