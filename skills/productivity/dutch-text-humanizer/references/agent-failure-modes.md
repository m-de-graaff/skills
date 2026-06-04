# Agent failure modes

Use this reference when the same humanizer skill performs differently across agents such as Claude, ChatGPT, Codex, or another model.

The fix is not to write separate prose rules for each model. The fix is to force every agent through the same review and validation gates.

## Common failure: polished strategic summary

Some agents produce text that is cleaner than the source but still detector-sensitive. It often looks like this:

- good paragraph rhythm, but still too polished
- no obvious chatbot residue
- too many abstract nouns: `propositie`, `regie`, `rendement`, `innovatie`, `informatievoorsprong`, `schaalbaar`, `leidende positie`
- too few practical VCS mechanisms
- benefits stated without enough ownership, system, team, cost, limitation, or operational consequence
- a partial natural-style match, not a strong one

This failure can pass a light text audit and still perform badly in external detectors.

## Claude-specific tendency observed

Claude may stop at a smooth management-summary voice. It often improves structure and removes obvious AI tells, but keeps phrases such as:

- `één organisatie voor vraagstukken`
- `diensten die terugkomen`
- `leidende posities`
- `voorspelbare, terugkerende omzet`
- `professioneel georganiseerd`
- `een vaste plek in het model`
- `het aanbod technologisch sterker`

Those phrases are not all forbidden. They become a problem when they carry the document instead of concrete operational detail.

## Hard delivery rule

For detector-focused Dutch work, do not deliver until:

```bash
python scripts/document_helper.py validate-humanized output.docx --corpus natural
```

passes.

Default gates:

- risk score <= 10
- abstract density <= 2.0 per 100 words
- consulting density <= 0.25 per 100 words
- concrete anchor density >= 14.0 per 100 words
- natural-style score >= 75 when `natural/` exists
- no text-audit findings

If any gate fails, rewrite. Do not explain around the failure.

## Rewrite away from this

```text
Consultancy opent de deur naar langlopende diensten en voorspelbare omzet.
```

## Rewrite toward this

```text
Consultancy moet duidelijk maken welk probleem de klant probeert te voorkomen. Daarna pas wordt bepaald of meldkamer, SOC, NOC, software of beheer nodig is.
```

## Final self-check

- Did the rewrite add practical VCS mechanisms, or only different strategy words?
- Are abstract nouns below the hard gate?
- Are concrete anchors high enough?
- Does the natural-style comparison pass?
- Would a VCS reader recognize the wording as close to internal ICT, tender, or operations prose rather than consultant prose?
