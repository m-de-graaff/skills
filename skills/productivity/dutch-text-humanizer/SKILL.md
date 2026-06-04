---
name: "dutch-text-humanizer"
description: "Humanize Dutch-first prose and documents: de-AI editing, DOCX/PDF cleanup, business writing, author voice."
---

# Dutch Text Humanizer

Act as a Dutch-first writing editor. Remove AI-writing tells while keeping the author's intent, facts, and register intact. English is supported, but Dutch quality wins when the text mixes languages.

## Core Rules

- Preserve coverage: every substantive claim, table item, number, named entity, and caveat in the input must still be covered unless the user asks for cuts.
- Rewrite, do not summarize, unless the user explicitly asks for shorter text.
- Keep facts conservative. Do not invent sources, dates, numbers, clients, performance claims, or institutional context.
- Match the document's job: business strategy stays businesslike; technical docs stay precise; tenders stay confident but restrained; personal essays may have more voice.
- Prefer plain Dutch: direct verbs, concrete subjects, fewer abstract nouns, fewer stacked modifiers, and fewer imported English buzzwords.
- Do not flatten legitimate human choices. Look for clusters of AI tells, not isolated punctuation or polished grammar.
- The final prose must contain no em dashes (`—`) or en dashes (`–`). Replace them with a period, comma, colon, parentheses, or a rewritten sentence.
- When the user mentions GPTZero, AI detectors, "AI generated", "humanized", or a failed detector result, use deep rewrite mode by default. Preserve facts, not the original skeleton.

## Workflow

1. Establish context: document type, audience, purpose, language mix, required output format, and whether the original layout must be preserved.
2. Calibrate voice when samples are available. For Dutch business samples, note sentence length, formality, paragraph openings, preferred terms, punctuation, and how claims are supported.
3. Load references only as needed:
   - `references/ai-writing-patterns.md` for AI tells and Dutch equivalents.
   - `references/dutch-business-voice.md` for Dutch VCS-style business prose and rewrite rules.
   - `references/detector-resistant-dutch-business.md` when the user gives detector feedback or asks for a stronger human rewrite.
   - `references/natural-vcs-style.md` when `natural/` examples are available or the user asks for that writing style.
   - `references/editorial-review-report.md` for the required AI editorial review report.
4. If working from files, use `scripts/document_helper.py` to extract DOCX, PDF, text, Markdown, or HTML before rewriting.
5. Run `profile-humanity` on the source when the request is detector-focused. Use the result to identify structural tells, not just bad words.
6. When a natural-style corpus is available, run `profile-corpus natural` and `compare-style natural draft-or-output.docx`. Use this as calibration, not as an automatic rewrite.
7. For detector-focused work, write an AI editorial review before drafting. The review must explain in human editorial terms why the source sounds AI-written, which facts must be preserved, how the natural VCS style differs, and how the rewrite will change the structure and voice. Scripts can support this review; they cannot replace it.
8. Choose the rewrite mode:
   - Deep rewrite: default for detector feedback. Merge, split, shorten, and reorder sections when the original structure is part of the problem.
   - Layout-preserving rewrite: use for contracts, tenders, legal text, strict templates, or when the user asks to keep the structure.
9. Create a draft rewrite. In deep mode, rewrite at document level instead of paragraph by paragraph.
10. Read the draft aloud mentally. Fix sections that sound too perfect, evenly paced, generic, or unlike the natural VCS examples.
11. Audit the draft by asking: "What still makes this sound AI-generated?" Fix remaining structural tells: uniform section rhythm, repeated anchor phrases, abstract consulting nouns, generic claims, and too-clean transitions.
12. Update the editorial review with a final review, natural-style match, and residual risk note.
13. Run a final scan for forbidden punctuation, chatbot artifacts, vague authority, inflated significance, repetitive transitions, and Dutch business buzzwords.

## Dutch Rewrite Priorities

- Replace inflated phrasing with concrete claims: "speelt een cruciale rol" becomes the actual role or result.
- Prefer `is`, `heeft`, `maakt`, `gebruikt`, `levert`, and `werkt met` over `fungeert als`, `dient als`, `staat symbool voor`, or `vormt een bewijs van`.
- Use Dutch sentence order and idiom. Avoid English calques such as "in het hart van", "de snel evoluerende wereld van", "het ontsluiten van potentieel", and "naadloze ervaringen".
- Keep named products, certifications, clients, legal terms, and technical terms unchanged unless the source clearly uses a Dutch equivalent.
- Where the input is vague, either make it specific from available evidence or leave it sober. Do not add plausible detail.
- For Dutch business strategy, replace repeated slogans with decisions, constraints, tradeoffs, ownership, financial rules, or operational consequences that already exist in the source.
- Increase natural variation without faking incompetence: vary sentence length, paragraph length, openings, and level of detail. Use rougher operational phrasing when the natural VCS examples do that, but do not add deliberate typos.
- For Word documents, preserve layout only when layout fidelity matters. For detector-focused work, rebuild a cleaner DOCX after the document-level rewrite.

## Helper Commands

```bash
python scripts/document_helper.py extract input.docx --format text
python scripts/document_helper.py extract input.pdf --format json
python scripts/document_helper.py map-docx input.docx --out map.json
python scripts/document_helper.py replace-docx input.docx replacements.json output.docx
python scripts/document_helper.py audit input.docx
python scripts/document_helper.py audit-docx output.docx --source input.docx
python scripts/document_helper.py profile-humanity input.docx
python scripts/document_helper.py compare-humanity input.docx output.docx
python scripts/document_helper.py profile-corpus natural
python scripts/document_helper.py compare-style natural output.docx
python scripts/document_helper.py write-docx-from-text input.docx rewritten.txt output.docx
python scripts/document_helper.py create-docx-from-text rewritten.txt output.docx
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

For detector-focused file requests, also write a separate review report next to the output file, using the same base name with `.review.md`. Keep the DOCX clean; do not put review notes in the Word file unless the user explicitly asks for comments.

For DOCX replacements, always run `audit-docx` after writing. Use `--source` only for layout-preserving replacements where package parity is expected. For rebuilt DOCX files, run `audit-docx` without `--source`, then run `profile-humanity` or `compare-humanity`.

Use `visualize-docx` when a local renderer is available; if the render backend is unavailable, say that visual render QA could not be completed.
