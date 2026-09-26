# Canon Q&A knowledge test: result (2026-09-25)

**Question.** Does a strong model already know what the Canon's books say, without being given the Canon?
The answer tells us which parts of the Canon are worth giving the writer: only what it does not already know.

**Cost.** US$0 of API spend. Claude sub-agents inside a Claude Code session (subscription). Nothing was paid to
media or LLM providers.

## Method

- **Items.** 345 of the 1,028 grounded Q&A items in `canon/qa/canon-014`. That is 15 per book across 23 books, stratified: up to 7 application items (a new case not in the book) and the rest knowledge-of-the-book items. The sample seed is in the script; the list is `sample.json`.
- **Answering.** Four blind Claude answerer agents each saw only their questions (book title + question). They had no Canon, no files and no web. They answered in 40–120 words and marked guesses "[unsure]".
- **Grading.** Four separate blind grader agents compared each answer with the book's reference answer:
  - 2 = the key points are right;
  - 1 = partial, or generic where the book is specific;
  - 0 = wrong, contradicts the book, or is filler.
- **Files.**
  - `answers-*.json`, `grades-*.json`: the raw answers and grades;
  - `by_item.json`: everything joined;
  - `RESULT-TABLES.md`: all breakdowns;
  - `analyse.py`: reproduces the tables.

## Result

| | Knows it (2) | Partial (1) | Wrong (0) |
|---|---|---|---|
| **All 345** | **25%** | **52%** | **23%** |
| Application (new case) | 19% | 63% | 18% |
| Knowledge of the book | 30% | 44% | 26% |

- **Self-flagged "[unsure]":** 64% of answers.
- **Best-known books:** Sontag (80%), Kahneman *Noise* (77%), Carroll (67%), WCAG (63%).
- **Least-known books:** Airey logo design, Freeman *Photographer's Eye*, Parameswaran, Jain *Gods in the Bazaar*, Hopkins ch 8–21 (37–40%).
- **Ad-craft sources in between:** Ogilvy-beyond (43%), Sullivan (50%), Google ABCD (53%).

## What it means

1. **The model knows the gist but not the book.** In about 77% of answers it had the general idea, and in only 25% did it have the book's specific position. My earlier working assumption, that "the model already knows most of the Canon", was **wrong at the level of specifics**. It holds only at the level of general principles.
2. **Much of what it misses doesn't matter for making ads.** Reading the "missed" notes, a large share is:
   - bibliographic detail, such as exact test figures from 1920s mail-order;
   - scholarly nuance ("the source never resolves this tension", "the evidence is weak here").

   The Q&A bank was written like a research exam, so a low score overstates the practical gap.
3. **Some misses are real, usable craft.** Examples:
   - Sullivan: "yeah right" objections need proof, "so what" objections need relevance.
   - Hopkins: friction for the customer raises response cost 3–4×.
   - Freeman: an eyeline works through curiosity.
   - Parameswaran: children *veto* some purchases and *pick* others.

   Indian-market books sit near the bottom, as expected. **This subset is what the gap card should contain.**
4. **Application questions** (a new case to reason about) were rarely fully right (19%) but rarely wrong (18%). The model reasons sensibly but misses the book's specific move. That is the knowing-vs-doing gap again.

## Consequences for Canon shape v1

- **The gap card** (piece 2) is built only from misses that would change a real ad decision. A blind classifier rewrites each as a one-line rule; see `canon/shape-v1/GAP-CARD.md`.
- **The general principles the model does know** (brand early, conflict, product as hero…) stay as **required decisions and a checklist**, not as reading (pieces 1 and 3). The model knows them and skips them.
- **Nothing here shows that giving the writer this knowledge improves finished media.** That is the P vs P+Canon arm of the media test.

## Limits

- **One answering model (Claude).** If the chef is GPT-5.6 Sol, the gap is Sol's and should be re-measured.
- **One grader pass per item, with no human spot-check yet.** A model grader may be strict or lenient. Spot-check about 20 items before relying on per-book numbers.
- **15 items per book,** so per-book scores have wide error bars (±25 points).
- **Book titles were shown to the answerer,** as the questions reference authors. That tests recall of the book, which is the intended question.
- **920 of the 1,028 bank items come from books still on hold,** not accepted Canon. The sample follows the bank (270 hold, 75 accepted).
