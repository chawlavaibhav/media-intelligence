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
]

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
