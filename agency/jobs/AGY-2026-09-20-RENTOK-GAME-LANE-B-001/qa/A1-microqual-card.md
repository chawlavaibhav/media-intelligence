# Micro-qualification card — A1 character sheet (att-018, gen/stills/A1_character_sheet_v1.png, sha256 9bb97e3a9871ce33f62350131c5a6aab8750c389beb7ad8c4e91373192ffc270)

Producer inspection (OBSERVED on the image; the independent checker re-inspects the same file):

| # | check | result | note |
|---|---|---|---|
| 1 | one identity across all nine cells (face, hair, glasses on head, ochre checked shirt, grey trousers, chappals, key ring, red register) | PASS on identity; **CORRECTED (Stage-5 checker, D-4): the red register is present in 6 of 9 cells and ABSENT in jump (cell 5), hurt (cell 6) and cornered (cell 7)** | my original wording "every cell carries every identifier" was wrong; repaired in repair round 1 by compositing a code-drawn register on those three cells (`tools/repair_sprites.py` → `gen/sprites/A1_{jump,hurt,cornered}_reg.png`) |
| 2 | no cap, no moustache, no overalls, no gloves | PASS | clean-shaven, bare head with glasses pushed up |
| 3 | no lettering, digits, labels, grid lines, watermark | PASS | none seen at 1024 px; phone screens plain blue |
| 4 | flat solid magenta background, keyable | PASS | uniform #FF00FF-class background, no shadows |
| 5 | side view facing right, full body, same proportions | PASS | consistent three-quarter-side view, ~6 heads |
| 6 | pose set complete (run 1–4, jump, hurt, cornered, powered-run A, powered-run B) | PASS with note | jump, hurt, cornered and both phone-raised poses are distinct; the four run cells differ only slightly in leg phase — the run cycle will read as motion mainly through the code-side bob/tilt and the scroll, not through the model's leg phases (recorded; a re-draw was NOT spent because the identity, keying and IP checks are the gated items) |

Verdict (producer): PASS — frozen as the only source of character pixels. Nintendo drift: none (no plumber cues). Repair allowance unused.
