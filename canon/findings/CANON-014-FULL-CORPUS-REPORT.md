# CANON-014 — Full corpus report

**Branch:** `work/canon-014-final-full-canon`, cut clean from `main` at `bf02dd1`.
**Not merged. One merge decision, not another reconciliation round.**

This is the plain-English account of what the Canon now contains. Counts come from
`canon/knowledge/CANON-CORPUS-INDEX.yaml`, which is generated from the artifacts, not typed by hand.

---

## The short version

The Canon now holds **42 sources**. **24 are accepted** — audited, and live. **18 are held** — kept
in full, structurally sound, and explicitly not admitted. Nothing was thrown away to get here.

| | Accepted | Held | Total |
|---|---|---|---|
| Sources | 24 | 18 | **42** |
| Source-knowledge objects | 677 | 839 | **1,516** |
| Concept systems | 78 | 72 | **150** |
| Operational bindings | 152 | 188 | **340** |
| Ontology terms | 589 | 841 | **1,430** |
| Ontology concepts | 67 | 118 | **185** |
| Q&A items | 108 | 920 | **1,028** |

**More than half the knowledge in this repository is held, not accepted.** That is the single most
important sentence in this report. It is not a failure — held knowledge is real knowledge whose
representation has not been verified — but anyone reading a total without the split will
substantially overstate what the Canon has established.

---

## What "accepted" and "held" actually mean

**Accepted** means a source passed the Audit Gate: somebody looked at the actual artefact, wrote down
what the copy could and could not show, and signed a record against the exact bytes of the
extraction. If those bytes change, the record goes stale and says so. Accepted sources live in
`canon/knowledge/current/`.

**Held** means the knowledge was extracted carefully and *its representation has not been verified*.
Held sources live in `canon/candidates/canon-014/`. Each carries an `audit-assessment-HOLD.yaml`,
which is deliberately **not** an Audit Gate record — different shape, different name, outside the
audit directory — because in this repository the existence of a record is what reads as admission.

**All 18 held sources now pass the same structural validator the accepted ones do, with zero errors.**
That is worth having and it is not admission. It says the files are well formed. It says nothing
about whether what they record was checked against the book.

---

## Why held knowledge is kept rather than deleted

Three reasons, and the third is the one that matters most.

1. **The knowledge is real.** *Noise* on how human judgement varies, Sullivan on concept versus
   execution, WCAG's legibility criteria — none becomes wrong because nobody has inspected the
   figures in that copy.
2. **The blockers are mostly fixable.** Most of them are one visual pass away from resolution.
   Deleting the extraction would mean redoing all of it to fix a much smaller gap.
3. **Deleting it would hide a real gap.** If the 17 sources vanished, the repository would look like
   a clean 24-source Canon. Keeping them makes it obvious that a large body of extracted knowledge is
   waiting on verification — which is true, and which the Controller needs to see to decide what to
   fund next.

The discipline that makes this safe is that **held never quietly becomes accepted**. A held source
has no audit record, its Q&A says `source_status: hold` on every item, the corpus index states its
status, and the Q&A validator refuses a bank that claims `accepted` for a source sitting in the
candidate tree.

---

## What the Indian-source expansion materially adds

Five books, all now accepted, all with first-hand visual work. This is the corpus's **first Indian
material of any kind**, and it is deliberately bounded.

- **Ambi Parameswaran, *Nawabs, Nudes, Noodles*** — Indian advertising history from inside the
  agencies, with **19 of 19 reproduced advertisements inspected first-hand**. Six craft mechanisms in
  it exist only because the plates were opened; four captions turned out **not** to be settled by
  their own plates, which a text-only pass would have transcribed as fact.
- **Piyush Pandey, *Pandeymonium*** — a practitioner's account of Indian creative work, with an
  unusually clean statement of what group self-report gets wrong and why observing attention beats
  asking about it. Its campaigns are not in the book: the publisher put them on a website, so every
  claim about a campaign is a claim about what Pandey *says* about it.
- **Dwyer & Patel, *Cinema India*** — how a Hindi-film poster carries a plot **without text**, using a
  compression code the viewer already holds; and a design problem this project had no name for:
  re-release publicity targets what an audience *retains*, not what the film was originally sold on.
- **Kajri Jain, *Gods in the Bazaar*** — the most operationally useful of the five. A fully documented
  case of a production convention outliving the constraint that produced it; a structural account of
  why a purchase signal is not a preference signal when the purchaser is not the viewer; and a
  distinction between an *enabling condition* and a *grading criterion* that our evaluation work
  lacked a name for.
- **Rama Bijapurkar, *We Are Like That Only*** — a set of named reasoning errors with worked cases,
  deliberately stripped of every number: reading a supply-side change as a consumer trait; planning
  on a segment label with no stated definition or population base; extrapolating a released stock as
  though it were a flow.

**The bound that must travel with all of it:** *Cinema India* dates its own subject as ending in the
1990s, *We Are Like That Only*'s data is 2008, and Jain's fieldwork runs to about 2006. What the
corpus gained is **carefully bounded historical Indian visual and market culture — not a current
picture of India.**

---

## What the earlier 17-source expansion materially adds

Held, and substantial: **839 source-knowledge objects, 188 bindings, 920 Q&A items** — more raw
knowledge than the accepted corpus contains.

- **Judgement and evaluation.** *Noise* is the only source anywhere in the corpus about how human
  judgement of the same artefact actually behaves. *Discussing Design* supplies the practitioner-side
  remedy. Together they bear directly on evaluator design, which is live work here.
- **Accessibility with real numbers.** WCAG 2.2 is the corpus's **only** standards document and its
  only source of numeric criteria — contrast ratios, resize percentages, spacing multipliers.
- **Short-form and feed-native.** Google's ABCD guidance is the only source addressing how a feed
  behaves, and is also the most platform-contingent thing in the corpus.
- **Effectiveness, contested.** Ries & Ries against the live Binet & Field material, on five points,
  recorded and unresolved.
- **Five scope extensions** — Hopkins, Light: Science & Magic, Samara, Ogilvy, Freeman — that read
  further into books already in Canon. Their value is largely **evidence about accepted sources**
  rather than new origins.

---

## What remains weak

- **Over half the corpus is unverified**, as above.
- **17 sources have never had a figure looked at.** In several the figures *are* the argument.
- **Airey's only copy is a bad translation** — an unattributed, degraded Spanish machine translation
  that on one page calls a *failed* redesign a successful one, contradicting its own body text.
- **Sullivan's independence is unresolved** against live Ogilvy, which blocks promotion until settled.
- **Live Canon may be carrying withdrawn guidance.** *Light: Science & Magic*'s later chapters demote
  a live chapter-3 remedy to "a solution to avoid whenever possible" and reverse a recommended order.
  The live record does not know this.
- **Three defects sit in accepted live Canon**, all pre-existing and none introduced here: three
  concept systems in `sutherland-alchemy-introduction` have no `provenance` block. Repairing them
  requires reopening the book, which stales the audit, which needs authorisation.
- **Nothing in the corpus is a measurement of a current model.** By design — that is the Capability
  Registry's job — but it means Canon can say what a good outcome requires and never which tool
  delivers it.

---

## What visual evidence exists

**25 of 42 sources have a visual-evidence ledger. 17 have never had an inspection run at all**, and
their ledgers are absent rather than empty — the honest state, because a ledger records what an
inspection found and writing one from a previous run's self-report would be fabricating an
inspection.

| Source | Coverage |
|---|---|
| Parameswaran | **19/19 plates**, complete |
| Bijapurkar | **30/30 data figures**, complete |
| Cinema India | 11 of ~121 plates; **7 authorial visual claims checked, all held** |
| Gods in the Bazaar | 7 of ~156 figures; **7 claims checked, all held** |
| Desai | completed with a null result — the book makes no visual argument |
| Pandey | completed; the campaigns were never printed in the book |
| The 17 | **none** |

Cinema India and Gods in the Bazaar were **bounded by cost, not blocked** — both copies are intact
and any figure can be rendered on demand — and their ledgers say so, as a coverage statement rather
than as a loss pattern, because nothing is missing from either copy.

**The most valuable single finding of the whole visual programme** came from Bijapurkar: that copy
preserved the prose as text and **every table and figure as a raster image**, so their content is
absent from the extracted text stream while the running prose names them and reasons from them. A
text-only extraction would have met every assertion, never met the evidence, and shown no sign of the
loss. At least nine tables carry content found nowhere in the text. **That is durable Canon knowledge
about how a source can be represented — not a claim about consumers.**

---

## What Q&A exists

**1,028 items across 23 banks**, at `canon/qa/canon-014/`. 108 from accepted sources, 920 from held
ones. **418 items (40.7%)** require applying the source to a new case — observed, never required; the
old one-third quota is gone.

**Grounded, ungraded, uncalibrated.** Every item traces to one source with a locator and a supporting
quotation. **No human and no model has answered a single one.** It is not benchmark ground truth, not
human-calibrated truth, not model-evaluation evidence, and not proof that Canon improves any outcome.

Nothing was removed. The screen found no duplicate id, no duplicate question, no malformed item and
no answer under the floor. One item was **amended**, because a source correction made in this
reconciliation made part of its answer wrong.

---

## The corpus fingerprints

Three, deliberately separate, so a future Canon-vs-no-Canon experiment can name exactly what it ran
against. **They are not interchangeable**: an experiment that ran against held knowledge is not an
experiment about accepted Canon.

| Fingerprint | Files | SHA-256 |
|---|---|---|
| **Accepted Canon** | 120 | `a9cee40fb433adc08ac98ba7c87e1ead790f60aa71d184327cc5e97f59ed7eb9` |
| **Full knowledge corpus** | 193 | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` |
| **Q&A corpus** | 23 | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` |

Generated at commit `e281059`; regenerate with `python3 canon/knowledge/build_corpus_index.py`.

---

## A change of fact the Controller should see

The earlier passes held the 17 partly because **the source could not be opened**: the extraction had
read a local library that did not exist in the container the repair ran in, and that container had no
network access. Both were true there.

**Neither is true here. 15 of the 17 books are on this machine, and network egress works.**

So the remaining blocker for most of them is not access — it is that **the inspection has not been
done**. That is cost and authorisation, which is a materially better position than being blocked, and
it is not a pass. This task did not run those inspections: it is a reconciliation, and promoting 17
sources on its own judgement is not its call.

**What this makes possible:** most of the 17 are now one authorised visual pass from a real admission
decision. The two worth doing first are *Light: Science & Magic beyond ch.3*, because live Canon may
currently be giving consumers guidance its own source later withdrew, and the *Noise* /
*Discussing Design* pair, because it bears directly on evaluator design that is live work now.
