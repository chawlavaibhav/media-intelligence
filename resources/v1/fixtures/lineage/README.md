# Lineage negative-control fixtures (R-C4)

`lineage-negative-control-manifest.jsonl` is a **36-row synthetic manifest**. Nothing in it is real
media: the item ids, paths and hashes are generated, and no file exists behind any of them. It exists
so the three lineage outcomes can be tested without touching the real corpus.

It contains six sources of three kinds:

| Sources | Kind | Expected outcome in a protected comparison |
|---|---|---|
| `src_bstd_devanagari`, `src_konvid1k` | **registered, genuinely independent lineages** | `PASS` — exit 0 |
| `src_indicstr12_devanagari`, `src_iiit_ilst_devanagari` | **registered, one shared lineage** (`lin_cvit_iiit_hyderabad`) | `LEAK` — exit 1 |
| `src_unregistered_example`, `src_unregistered_other` | **unregistered: lineage not established** | `INDETERMINATE` — exit 3 |

The third row is the point of R-C4. Two unregistered sources produce two *different*
`lin_unknown::` keys, and a naive comparison would call them independent. They are not known to be
independent — they may be the same lab, the same collection effort, or one derived from the other,
and nothing in a source id says otherwise. **The tool must refuse to certify rather than certify.**

Run them with `../../validators/run_lineage_negative_controls.sh`.
