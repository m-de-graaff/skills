# AI Writing Patterns

Use this reference as a checklist, not as a mechanical find-and-replace list. One signal rarely proves anything. Rewrite when multiple patterns cluster or when a phrase weakens the prose.

## Dutch-first patterns

| Pattern | Dutch signals | Rewrite direction |
|---|---|---|
| Inflated significance | `cruciaal`, `essentieel`, `toonaangevend`, `sleutelrol`, `pivotaal`, `markeert een belangrijke stap`, `onderstreept het belang` | State the actual fact, role, decision, result, or dependency. |
| Symbolic padding | `staat symbool voor`, `vormt een bewijs van`, `is een toonbeeld van`, `weerspiegelt bredere ontwikkelingen` | Remove unless symbolism is the subject and evidence exists. |
| Promotional tone | `krachtig`, `innovatief`, `baanbrekend`, `uniek`, `veelzijdig`, `naadloos`, `robuust`, `state-of-the-art`, `rijk`, `dynamisch` | Keep concrete capabilities, numbers, and constraints. |
| Vague authority | `experts stellen`, `onderzoek toont aan`, `marktpartijen zien`, `men verwacht`, `volgens diverse bronnen` | Name the source or remove the authority claim. |
| Present participle padding | `waarbij`, `zodat`, `gericht op`, `resulterend in`, `bijdragend aan`, `ondersteunend aan` chains | Split sentences and make the actor/result explicit. |
| Copula avoidance | `fungeert als`, `dient als`, `vormt`, `positioneert zich als`, `biedt een platform voor` | Use `is`, `heeft`, `maakt`, `levert`, `gebruikt`, `beheert`. |
| Rule of three | Forced lists of three benefits, values, or adjectives | Keep only useful distinctions; do not pad for rhythm. |
| Abstract landscapes | `landschap`, `ecosysteem`, `reis`, `transformatie`, `potentieel ontsluiten`, `waardepropositie` | Use the real domain word: markt, systeem, proces, planning, investering, klantvraag. |
| Fake contrast | `niet alleen ..., maar ook`, `het gaat niet alleen om`, `meer dan alleen` | Say the point directly. |
| Generic conclusion | `de toekomst ziet er rooskleurig uit`, `een belangrijke stap voorwaarts`, `op weg naar succes` | End with a decision, risk, next action, or factual consequence. |
| Chatbot residue | `natuurlijk`, `zeker`, `ik hoop dat dit helpt`, `laten we`, `hier is een overzicht` | Remove. Content should not narrate the assistant. |
| Knowledge disclaimers | `op basis van beschikbare informatie`, `voor zover bekend`, `details zijn beperkt beschikbaar` | Cite what is known or state soberly that it is not documented. |
| Hedging pileups | `mogelijk`, `potentieel`, `zou kunnen`, `in zekere mate`, `waarschijnlijk wellicht` | Keep the one hedge that is factually needed. |
| English buzzword stacking | `data-driven`, `end-to-end`, `cross-functioneel`, `customer journey`, `seamless`, `scalable` | Use Dutch where natural; keep English only for established product or sector terms. |

## Supplied English base patterns

Also watch for these English patterns, especially in mixed-language source text:

- Undue emphasis on significance, legacy, broader trends, or "evolving landscapes".
- Notability padding through media-name lists without specific claims.
- Superficial `-ing` analyses: `highlighting`, `ensuring`, `reflecting`, `showcasing`.
- Advertisement-like language: `boasts`, `vibrant`, `rich`, `profound`, `renowned`, `stunning`.
- Vague attribution: `industry reports`, `observers`, `experts argue`, `several publications`.
- Formulaic challenge/future sections with "despite these challenges".
- High-frequency AI vocabulary: `delve`, `crucial`, `pivotal`, `underscore`, `tapestry`, `testament`, `intricate`, `valuable`, `vibrant`.
- Avoidance of simple `is`, `are`, and `has`.
- Negative parallelisms: `not only... but`, `not just about...`.
- Synonym cycling instead of useful repetition.
- False ranges: `from X to Y` when X and Y are not a real scale.
- Passive voice or subjectless fragments when the actor matters.
- Boldface overuse, inline-header bullet lists, emoji bullets, title-case headings, and curly quotation marks.
- Persuasive authority tropes: `the real question is`, `at its core`, `what really matters`.
- Signposting: `let's dive in`, `here's what you need to know`.
- Fragmented headers: a heading followed by a one-line restatement before the real content.
- Diff-anchored writing in stable docs: "this was added to replace..." instead of describing the current behavior.

## Hard cleanup checks

- No em dashes or en dashes in the final rewrite.
- No emojis unless the original is social or informal content and the user wants to keep them.
- No unsupported claims added during rewriting.
- No fake specificity. If a detail is unknown, do not invent it to make the text sound human.
- No needless title case in Dutch headings. Use sentence case unless a proper name requires capitals.

## False positives

Do not over-edit just because text is polished. Preserve:

- Specific details that look hard to fabricate.
- Mixed feelings or unresolved tension.
- Era-bound references, internal terms, names, and context.
- Legitimate formal Dutch needed for tenders, policy, contracts, or board documents.
- Repetition where consistency matters: product names, legal terms, technical controls, certifications.
- A single dash, transition, or formal word when the surrounding prose is otherwise natural.
