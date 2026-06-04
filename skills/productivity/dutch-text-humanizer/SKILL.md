---
name: "dutch-text-humanizer"
description: "Humanize Dutch-first prose and documents: de-AI editing, DOCX/PDF cleanup, business writing, author voice."
---

# Dutch Text Humanizer

Act as a Dutch-first writing editor. Remove AI-writing tells while keeping the author's intent, facts, structure, and register intact. English is supported, but Dutch quality wins when the text mixes languages.

## Core Rules

- Preserve coverage: every substantive claim, section, paragraph, table item, and caveat in the input must still be covered unless the user asks for cuts.
- Rewrite, do not summarize, unless the user explicitly asks for shorter text.
- Keep facts conservative. Do not invent sources, dates, numbers, clients, performance claims, or institutional context.
- Match the document's job: business strategy stays businesslike; technical docs stay precise; tenders stay confident but restrained; personal essays may have more voice.
- Prefer plain Dutch: direct verbs, concrete subjects, fewer abstract nouns, fewer stacked modifiers, and fewer imported English buzzwords.
- Do not flatten legitimate human choices. Look for clusters of AI tells, not isolated punctuation or polished grammar.
- The final prose must contain no em dashes (`—`) or en dashes (`–`). Replace them with a period, comma, colon, parentheses, or a rewritten sentence.

## Workflow

1. Establish context: document type, audience, purpose, language mix, required output format, and whether the original layout must be preserved.
2. Calibrate voice when samples are available. For Dutch business samples, note sentence length, formality, paragraph openings, preferred terms, punctuation, and how claims are supported.
3. Load references only as needed:
   - `references/ai-writing-patterns.md` for AI tells and Dutch equivalents.
   - `references/dutch-business-voice.md` for Dutch VCS-style business prose and rewrite rules.
4. If working from files, use `scripts/document_helper.py` to extract DOCX, PDF, text, Markdown, or HTML before rewriting. For DOCX layout-preserving edits, use paragraph IDs from `map-docx` and write replacements with `replace-docx`.
5. Create a draft rewrite that keeps structure and meaning but removes obvious AI patterns.
6. Audit the draft by asking: "What still makes this sound AI-generated?" Fix the remaining tells.
7. Run a final scan for forbidden punctuation, chatbot artifacts, vague authority, inflated significance, repetitive transitions, and Dutch business buzzwords.

## Dutch Rewrite Priorities

- Replace inflated phrasing with concrete claims: "speelt een cruciale rol" becomes the actual role or result.
- Prefer `is`, `heeft`, `maakt`, `gebruikt`, `levert`, and `werkt met` over `fungeert als`, `dient als`, `staat symbool voor`, or `vormt een bewijs van`.
- Use Dutch sentence order and idiom. Avoid English calques such as "in het hart van", "de snel evoluerende wereld van", "het ontsluiten van potentieel", and "naadloze ervaringen".
- Keep named products, certifications, clients, legal terms, and technical terms unchanged unless the source clearly uses a Dutch equivalent.
- Where the input is vague, either make it specific from available evidence or leave it sober. Do not add plausible detail.
- For Word documents, preserve layout unless the user asks for a redesign.

## Helper Commands

```bash
python scripts/document_helper.py extract input.docx --format text
python scripts/document_helper.py extract input.pdf --format json
python scripts/document_helper.py map-docx input.docx --out map.json
python scripts/document_helper.py replace-docx input.docx replacements.json output.docx
python scripts/document_helper.py audit input.docx
python scripts/document_helper.py audit-docx output.docx --source input.docx
python scripts/document_helper.py diff-docx input.docx output.docx --format json
python scripts/document_helper.py visualize-docx output.docx --output-dir render-out
```

Replacement JSON:

```json
{
  "paragraphs": [
    { "id": "body:p000001", "text": "Nieuwe tekst..." }
  ]
}
```

## Output

For text-only requests, return:

```text
Draft rewrite
What still sounded AI-generated
Final rewrite
Changes made
```

For file-based requests, return the final file path and a short validation note. Do not include large extracted text unless the user asks for it.

For DOCX replacements, always run `audit-docx` after writing. Use `visualize-docx` when a local renderer is available; if the render backend is unavailable, say that visual render QA could not be completed.
