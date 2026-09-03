"""Recogniser vocabularies for the gate (CANON-GATE-001 plan §B.1 and §D).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

These constants are implementation, not doctrine: each is annotated with the check_id it
serves and, where the plan says so, the pack words it extends. Terms are written in
regex-ready form (`s?` plurals, `\\s+` for spaces) and are matched case-insensitively at
word boundaries by textscan.compile_terms. Tuning any constant is a Controller-visible
change: append a line to CHANGELOG with the date, the constant and the reason.
"""

CHANGELOG = [
    "2026-09-03 v0: constants transcribed from GATE-BUILD-PLAN-v0 §B.1 and §D as written.",
    "2026-09-03 F-04: ASPECT_CONTEXT_WORDS / TIME_CONTEXT_BEFORE / TIME_CONTEXT_AFTER added — "
    "a `\\d:\\d` pair with clock-time context ('Hands set to 10:10 as convention.', 'the "
    "logo holds for the last 0:03', 'Time must read ~10:10') is not an aspect; aspect context "
    "('4:5 aspect ratio', 'Vertical 9:16', '(9:16)') wins over time context.",
    "2026-09-03 F-07: NEGATED_AFTER added for CA-D2 clause 2 — the negation window for a named "
    "ratio is the whole sentence before the term plus an 'is not / is avoided' disclaimer right "
    "after it ('We will not compose this using the rule of thirds.', 'Avoid any reliance on the "
    "classic rule of thirds.', 'The rule of thirds is not used here.'). T2/T3 keep the 4-token "
    "window.",
]

# ── §B.1 recognisers for the partial pre-dispatch checks ────────────────────────────────
# PA-D1 — pack words: diffuse, matte, direct, glossy, glare — extended per the plan.
FINISH_TERMS = (
    "diffuse", "matte", "direct", "glossy", "glare",
    "gloss", "polished", "brushed", "satin", "mirror", "sheen", "specular", "reflective",
    "frosted", "lacquer", "metallic",
)
# PA-D4 — a LIGHT term and a DIRECTION term in one sentence.
LIGHT_TERMS = (
    r"key\s+light", "key", r"light\s+source", "softbox", r"soft\s+box", r"window\s+light",
    "daylight", "sunlight", "tube-light", "tubelight", "lamp", "practical", "backlight",
    r"rim\s+light", "kicker", "fill", "spotlight", r"overhead\s+light", r"lit\s+from",
    r"light\s+from",
)
DIRECTION_TERMS = (
    "upper-left", r"upper\s+left", "top-left", r"top\s+left", "upper-right", r"upper\s+right",
    "top-right", r"from\s+the\s+left", r"from\s+the\s+right", r"from\s+above", r"from\s+behind",
    r"from\s+the\s+side", "camera-left", "camera-right", "overhead", "behind", "side", "front",
    r"\d+\s*°", r"\d+\s*degrees", "window",
)
# PA-D8 — conditional: a GLOSSY-SURFACE term requires a SPECULAR-DECLARATION term.
GLOSSY_SURFACE_TERMS = (
    "glass", "crystal", "sapphire", "bottle", "mirror", "chrome", "polished", "glossy",
    "lacquer", "black", r"dark\s+surface", r"dark\s+background",
)
SPECULAR_DECLARATION_TERMS = (
    "reflection", "reflections", "specular", "speculars", "highlight", "highlights", "glint",
    "glare",
)
# CA-D1 — an ordered enumeration of >= 3 reads (each family must show all three ranks).
READ_ORDER_NUMBERED = r"^\s*(?:[-*]\s*)?(?:\*\*)?{n}[.)]"
READ_ORDER_ORDINAL = r"\b{n}\s+read"                   # 1st / 2nd / 3rd read
READ_ORDER_RANK = r"\b{n}\b"                           # Primary / Secondary / Tertiary
# CA-D2 clause 2 — deliberately excludes bare "third" / "lower third" / "upper-middle third"
# (zone descriptions in the accepted B06 package).
NAMED_RATIO_GRID_TERMS = (
    r"rule\s+of\s+thirds", "rule-of-thirds", r"thirds\s+grid", r"golden\s+ratio",
    r"golden\s+section", r"golden\s+mean", r"golden\s+spiral", r"divine\s+proportion",
    "fibonacci", r"phi\s+grid", r"grid\s+line", "gridline", r"intersection\s+of\s+the\s+thirds",
    r"power\s+point", r"power\s+points",
)
# CA-D2 clause 1.
PLACEMENT_TERMS = (
    "centre", "center", "off-centre", "off-center", r"left\s+of\s+centre", r"left\s+of\s+center",
    r"right\s+of\s+centre", r"right\s+of\s+center", "upper", "lower", "zone", "positioned",
    "placed", "placement",
)
# CA-D5 — deliberately excludes "symmetrical" ("clean symmetrical dial layout" is the dial).
BALANCE_TERMS = ("balanced", "balance", "restless", "unbalanced", "off-balance",
                 r"refuse\s+the\s+eye")
# CA-D6 — alongside package.ASPECT_RATIO (`\b\d{1,2}:\d{1,2}\b`).
ASPECT_WORDS = ("square", "portrait", "landscape", "vertical", "horizontal")
# CA-D6 / DISPATCH-ASPECT (F-04): a `\d:\d` pair is an aspect unless it reads as a clock time.
# Within 3 tokens either side, an aspect-context word accepts it; otherwise a time-context
# word before it (or a time suffix after it), a leading zero, or a zero numerator rejects it.
ASPECT_CONTEXT_WORDS = frozenset((
    "aspect", "ratio", "vertical", "portrait", "landscape", "horizontal", "square", "format",
    "frame", "framing", "crop", "cropped", "video", "image", "still", "hero", "composition",
    "deliverable", "delivered", "execute",
))
TIME_CONTEXT_BEFORE = frozenset((
    "to", "set", "hands", "hand", "read", "reads", "reading", "showing", "shows", "show",
    "time", "times", "timestamp", "clock", "last", "first", "until", "till", "mark", "minute",
    "minutes", "second", "seconds", "hour", "hours", "o'clock", "around", "approx",
    "approximately", "by", "since", "before", "after", "between", "runs", "from", "at",
))
TIME_CONTEXT_AFTER = frozenset(("am", "pm", "o'clock", "mark", "timestamp", "sharp", "as"))
# PA-D10 — a DOCTRINE_DEVIATIONS entry names a decision id and carries a forcing clause.
DEVIATION_ID = r"\b(?:PA|CA)-D\d+\b"
DEVIATION_CLAUSE_WORDS = ("because", "brief")

# ── §D baked-text guard (LIMIT-TEXT; source: the verbatim pack limit line) ──────────────
# T2 (a): a quoted string of >= 2 word characters together with one of these verbs.
TEXT_VERBS = (
    "reading", "reads", "says", "saying", "labeled", "labelled", "titled", "text", "caption",
    "headline", "tagline", "subheading", "wordmark", "lettering", r"with\s+the\s+words",
    "displays", "displaying", "showing", "shows",
)
# T2 (b): a request for rendered text.
TEXT_REQUEST_TERMS = (
    "captions?", "subtitles?", "headline", "tagline", r"title\s+card", "typography", "lettering",
    "wordmark", "logos?", r"on-screen\s+text", r"text\s+overlays?", "watermarks?",
    r"text\s+reading", r"label\s+reading",
)
# A negator within 4 tokens before a T2 term clears it.
NEGATORS = ("no", "not", "never", "without", "avoid", "zero")
NEGATOR_PHRASES = ("rather than", "never a")
# CA-D2 clause 2 only (F-07): a disclaimer immediately after a named-ratio term also clears
# it — "The rule of thirds is not used here." / "The golden ratio is deliberately avoided."
NEGATED_AFTER = (
    r"^\s*(?:is|are|was|were|will\s+be|be|gets?|remains?)\s+(?:\w+ly\s+)?"
    r"(?:not|never|avoided|rejected|ignored|unused|forbidden|banned|excluded|abandoned|dropped)\b"
)
# A deferral term anywhere in the sentence clears T2 (the text is composited, not drawn).
DEFERRAL_TERMS = (
    r"added\s+in\s+post", r"in\s+post", "post-production", "composited", "composite",
    "deterministic", r"overlay\s+later", r"reserved\s+for", r"space\s+reserved", r"to\s+be\s+added",
)
# T3: a text-bearing surface with no illegibility/deferral term in the same sentence.
TEXT_SURFACE_TERMS = (
    r"chat\s+bubbles?", r"chat\s+thread", "chats?", "conversations?", "messages?",
    "notifications?", "badges?", "counter", "spreadsheet", "excel", r"#REF", "ledger",
    "notebook", "handwritten", "sign", "signage", "chart", "poster", "receipt", "invoice",
    r"price\s+tag", "menu", "newspaper", "dashboard", r"app\s+icon", r"app\s+screen",
    r"home\s+screen", "UI", "interface", "button", "banner", r"phone\s+screens?",
    r"smartphone\s+screens?", r"laptop\s+screens?", r"screen\s+showing", r"screen\s+shows",
    r"screen\s+filling", r"screens\s+showing",
)
ILLEGIBILITY_TERMS = (
    "illegible", "unreadable", "blurred", r"out\s+of\s+focus", "blank", r"dark\s+screen",
    r"switched\s+off", r"screen\s+replacement", r"replaced\s+in\s+post", r"green\s+screen",
    "greenscreen", "placeholder", r"no\s+legible", r"no\s+readable", r"added\s+in\s+post",
    "composited",
)
# Detail line only (no status effect): does the prompt carry an explicit no-text clause?
NO_TEXT_CLAUSE = (
    r"\bno\b[^.;,\n]{0,24}?\b(?:text|lettering|typography|captions?|logos?|watermarks?|words)\b"
    r"|\btext[- ]free\b"
)
