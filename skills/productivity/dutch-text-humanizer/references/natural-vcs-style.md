# Natural VCS style

This reference distills the writing patterns from the local `natural/` DOCX examples. Do not commit those large source documents by default; use this file as the tracked style target.

## What the natural examples sound like

The natural VCS documents are not glossy marketing copy. They read like practical ICT, tender, operations, and management documents written by people close to the work.

Typical traits:

- Specific systems, tools, clients, standards, dates, modules, costs, people, and constraints appear early.
- Sentences vary a lot. Some are short and blunt. Others are long because the writer is explaining a real technical or organizational dependency.
- Paragraphs are uneven. There are titles, short notes, lists, explanations, and dense implementation paragraphs next to each other.
- The writing sometimes has rough edges: direct transitions, small asides, parentheses, quoted tool names, concrete warnings, and visible tradeoffs.
- Benefits are tied to a mechanism: monitoring, backup retention, asset modules, SIEM scope, OWASP, ISO-27001, port numbers, subscriptions, internal knowledge, or staffing.
- The voice is formal enough for business, but not polished into consulting language.

## Apply this style

- Start from the work, not the ambition. Say what VCS does, which system or team is involved, and why that matters.
- Use concrete detail from the source before abstract strategy words.
- Keep useful internal terms: Topdesk, Jira, NOC, SOC, VCS Observation, VCS Multimedia, KPN, Eurofiber, Azure, OWASP, ISO, AVG, FTE, rendement.
- Allow a practical aside when the source supports it, for example a cost concern, a limitation, or a dependency.
- Prefer "dit is nodig omdat..." over "dit versterkt het onderscheidend vermogen".
- Use lists where a human VCS document would use them: choices, requirements, scope boundaries, modules, or actions.
- Keep some texture. A perfectly balanced paragraph after every heading is suspicious here.

## Detector-focused manual checks

AI detectors are unreliable and can flag human writing, especially non-native or highly polished business prose. Do not promise a detector result. Still, these edits reduce common signals:

- Add source-specific detail and viewpoint instead of generic claims.
- Increase burstiness: mix one-line paragraphs with longer explanations.
- Change sentence openings. Avoid paragraph after paragraph starting with the same strategic frame.
- Rewrite from memory after reading the source. Do not paraphrase sentence by sentence.
- Read aloud. If it sounds like a brochure, board-slide narration, or consultant summary, rewrite it closer to the work.
- Use active voice mostly, but not mechanically. Natural Dutch business documents also use passive voice when ownership is less important.
- Do not add fake typos. Natural imperfections are rhythm, specificity, and practical digression, not deliberate mistakes.

## Bad direction

```text
VCS/COPE positioneert zich als een geïntegreerd platform dat structurele waarde creëert door schaalbare diensten te combineren met strategische regie.
```

## Better direction

```text
VCS/COPE moet eerder in het gesprek komen. Niet pas wanneer er camera's of beheeruren worden ingekocht, maar wanneer de klant nog bezig is met de vraag wie de opvolging organiseert en wie verantwoordelijk is als het systeem niet doet wat nodig is.
```

## Final style test

Before returning the rewrite, ask:

- Staat er genoeg concreets in om te geloven dat dit uit VCS komt?
- Heeft elke abstracte claim een mechanisme, eigenaar, systeem, norm, kostenpost, team of keuze?
- Zijn er korte en lange zinnen door elkaar gebruikt?
- Zijn sommige paragrafen bewust kort gehouden?
- Is het document nog zakelijk, maar minder glad?
