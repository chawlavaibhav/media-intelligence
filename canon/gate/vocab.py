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
    "2026-09-03 F-05: LIGHT_TERMS — bare `key` and `fill` removed ('the key is the product "
    "itself, shown from the front'); `key source`, `soft key`, `hard key`, `fill light`, "
    "`fill from`, `fill source` added so Sonnet B06's 'single large soft key … gentle fill "
    "from camera-right' still declares a source.",
    "2026-09-03 F-05: DIRECTION_TERMS — bare `side`, `front`, `behind`, `window` and bare "
    "`\\d°` / `\\d degrees` removed ('Soft window light.', 'shown from the front', 'dial "
    "tilted 5°'); `from the/a left|right|front|back|rear|top|bottom`, `from … window`, "
    "`side-lit`, `side light`, `front-lit`, `backlit`, `behind the <subject>` and "
    "`\\d° <above|below|from|camera-…>` added ('45° above horizontal', '45 degrees "
    "camera-left').",
    "2026-09-03 F-05: BALANCE_TERMS — bare `balance` removed ('brighter neutral daylight "
    "balance' is white balance; Sonnet B01 CA-D5 returns to the plan's FAIL); "
    "`compositional|visual|tonal|formal balance`, `balance of/in the frame|composition`, "
    "`in balance`, `imbalance` added.",
    "2026-09-03 F-02: TEXT_SURFACE_TERMS — bare `chats?`, `conversations?`, `messages?`, "
    "`counter`, `menu`, `button`, `banner`, `interface` removed ('two friends in conversation "
    "over chai', 'warm banner of cloud', 'a menu of soft greens', 'the counter of the kitchen "
    "island', 'pressing the crown button', 'the user interface is not visible'); qualified "
    "forms added (whatsapp chats/conversations/messages, chat window/screen/messages, text "
    "messages, message bubbles, unread messages, notification/unread/badge counter, "
    "restaurant menu / menu board / app menu, cta/app/download/on-screen/ui button, "
    "'button labelled', shop/ad/web/notification banner, banner ad/text, app/user/mobile "
    "interface). T3 now honours the 4-token negation window ('no secondary messages').",
    "2026-09-03 F-02: DISPLAY_VERBS split out of TEXT_VERBS — `displays`, `displaying`, "
    "`showing`, `shows` count under T2 rule (a) only when the sentence also carries a "
    "TEXT_SURFACE term ('A model showing the \'Aster Meridian 38\' on her wrist, no text "
    "anywhere' clears; 'The phone screen shows a notification alert: \'…\'' still hits).",
    "2026-09-03 F-02: ILLEGIBILITY_TERMS — `not visible`, `screen off`, `screen(s) is/are "
    "off|dark|black`, `powered off`, `turned off`, `off-screen`, `invisible` added ('the user "
    "interface is not visible; screen off'). NEGATOR_PHRASES — `free of`, `devoid of`, "
    "`absence of` added ('a plate free of text').",
    "2026-09-03 F-03: TEXT_REQUEST_TERMS — added `text on|across|along|over|around|at|in|…` "
    "('elegant text on the dial', 'add text across the top third'); `<verb> … text` "
    "(add/place/render/include/put/print/with/featuring/bearing …, not `text-free`); `the "
    "word(s)` and plural `letters` ('the word RENT in bold red letters', 'a placard with the "
    "words Save Time'); `model|brand|product|company|shop|store|business name`, "
    "`owner's|manager's|tenant's … name`, `bearing … name` ('the dial shows the model name', "
    "'a nameplate bearing the manager\'s name'); `engraved with`, `engraving`, `inscription`, "
    "`inscribed` ('caseback engraved with the model name'); `that|which says|reads` ('a label "
    "that says Aster'); `numerals`, `digits` ('a wall clock with clear numerals'); `phone|mobile|"
    "whatsapp|contact number`, `helpline` ('the phone number 98765 43210 painted across the "
    "shutter'); `url`, `web address`, `www.`, `<name>.com|in|co|ai|org|net|io`, `http(s)://` "
    "('a billboard with the URL www.rentok.com'); `written`, `hand-written`, `handwriting` "
    "('written in Hindi on the wall'); `slogan`, `motto`, `strapline`, plural `headlines|"
    "taglines` ('a t-shirt with a slogan'); `devanagari` (the limit line's own word); `cta`, "
    "`call to action`, `body copy`, `text link`, `text label`; a quoted string followed by "
    "button|tab|link|chip|badge|label|banner|toggle ('a \'Verify KYC\' button').",
    "2026-09-03 F-03: TEXT_SURFACE_TERMS — added `label(s)`, `placard(s)`, `calendar(s)`, "
    "`licen[cs]e|number|registration plate(s)`, `nameplate(s)`, `name plate(s)|board(s)`, "
    "`billboard(s)`, `hoarding(s)`, `signboard(s)`, `storefront`; bare `sign` widened to "
    "`sign(s)` but not `sign(s) of` ('signs of wear on the strap' is not a surface).",
    "2026-09-03 F-02/F-03 recorded misses (lexical rules, not semantics): bare `banner`, "
    "`menu`, `button`, `counter`, `message`, `conversation`, `chat`, `interface` no longer fire "
    "alone, so 'a banner hangs across the street', 'a menu on the table', 'a chat open on the "
    "laptop' are misses unless another term is present; 'in Hindi' alone is not a hit "
    "(dialogue prompts say 'speaking in Hindi'); a display verb with a quoted product name and "
    "no surface term is not a hit by design. Recorded over-fires: `label` fires on 'a wine "
    "bottle with its label' and `letters` on 'love letters on the desk' — both text-bearing, "
    "accepted; `written` fires on any 'written' outside a negation window.",
    "2026-09-03 K-01: CA-D2 clause-2 negation window bounded — the F-07 sentence-wide window "
    "is withdrawn; textscan.CA_D2_NEGATION_WINDOW = 6 tokens before the term (plan §B.1's 4 "
    "amended by Ruling 6 condition 1) plus NEGATED_AFTER. 'Without clutter, the watch sits on "
    "the golden ratio point.', 'No hard shadows, dial placed on the rule of thirds line.', "
    "'Not too tight, the crown sits at the intersection of the thirds.' FAIL; the F-07 "
    "phrasings still PASS.",
    "2026-09-03 K-03: GOVERNANCE_BREAK / GOVERNANCE_STOP_WORDS added — T3's 4-token negation "
    "window (F-02) clears a surface only when the negator governs it directly: no punctuation, "
    "gerund or preposition/conjunction between them ('Avoid cluttering the dashboard', 'never "
    "crowded, the poster on the wall', 'A tidy, not busy, receipt on the table', 'zero clutter "
    "around the invoice' HIT; 'no chat bubbles', 'no visible signage', 'not a dashboard', "
    "'a plate free of labels' still CLEAR). T2 keeps the plain window. Recorded over-fires: an "
    "adjectival gerund ('no glowing notifications') and 'avoid showing the receipt' now HIT.",
    "2026-09-03 K-06: TEXT_REQUEST_TERMS — `numerals?` / `digits` no longer fire after a "
    "DIAL_NUMERAL_QUALIFIER (arabic|roman|hour|date|dial|applied|luminous|minute|index): "
    "'Arabic numerals at 12, 3, 6 and 9 on the dial', 'the date digits at 3 o'clock', 'Roman "
    "numerals, no other markings' CLEAR; 'a wall clock with clear numerals' still HITs. "
    "TEXT_SURFACE_TERMS — `labels?` excludes `label-free` / `label-less` ('a label-free "
    "bottle' CLEARs); bare `storefront` narrowed to `storefront sign|signage|signboard|"
    "lettering|name|text|board` ('a quiet storefront at dusk, shutters down' CLEARs; 'storefront "
    "lettering' and 'the phone number … painted across the shutter' still HIT). Recorded "
    "misses, pinned: 'a wall clock with Roman numerals' and 'a busy storefront' CLEAR — the "
    "qualifier is the watch category's dial vocabulary and the gate cannot tell a dial from a "
    "wall clock lexically; the blocking direction is kept for unqualified numerals.",
]

# ── §B.1 recognisers for the partial pre-dispatch checks ────────────────────────────────
# PA-D1 — pack words: diffuse, matte, direct, glossy, glare — extended per the plan.
FINISH_TERMS = (
    "diffuse", "matte", "direct", "glossy", "glare",
    "gloss", "polished", "brushed", "satin", "mirror", "sheen", "specular", "reflective",
    "frosted", "lacquer", "metallic",
)
# PA-D4 — a LIGHT term and a DIRECTION term in one sentence.
# F-05: bare `key` / `fill` narrowed to lighting phrases.
LIGHT_TERMS = (
    r"key\s+light", r"key\s+source", r"soft\s+key", r"hard\s+key", r"light\s+source", "softbox",
    r"soft\s+box", r"window\s+light", "daylight", "sunlight", "tube-light", "tubelight", "lamp",
    "practical", "backlight", r"rim\s+light", "kicker", r"fill\s+light", r"fill\s+from",
    r"fill\s+source", "spotlight", r"overhead\s+light", r"lit\s+from", r"light\s+from",
)
# F-05: bare `side` / `front` / `behind` / `window` / `°` narrowed to direction phrases.
DIRECTION_TERMS = (
    "upper-left", r"upper\s+left", "top-left", r"top\s+left", "upper-right", r"upper\s+right",
    "top-right", r"from\s+the\s+left", r"from\s+the\s+right", r"from\s+above", r"from\s+behind",
    r"from\s+the\s+side", r"from\s+(?:the\s+|a\s+)?(?:left|right|front|back|rear|top|bottom)\b",
    r"from\s+(?:the\s+|a\s+)?(?:[\w/-]+\s+){0,2}windows?\b", "camera-left", "camera-right",
    "overhead", "side-lit", r"side\s*light(?:ing)?", "front-lit", "backlit",
    r"behind\s+the\s+(?:subject|product|watch|bottle|talent|set|dial)",
    r"\d+\s*(?:°|degrees)\s*(?:above|below|from|off|to\s+the|camera-?|left|right|top|upper|"
    r"lower|front|back|side|elevation|azimuth|high|up)",
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
# CA-D5 — deliberately excludes "symmetrical" ("clean symmetrical dial layout" is the dial)
# and, since F-05, bare "balance" ("daylight balance" is white balance).
BALANCE_TERMS = ("balanced", "restless", "unbalanced", "off-balance", r"refuse\s+the\s+eye",
                 r"(?:compositional|visual|tonal|formal)\s+balance",
                 r"balance\s+(?:of|in|across)\s+the\s+(?:frame|composition|image)",
                 r"in\s+balance", "imbalance")
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
)
# T2 (a), F-02: display verbs count only when the sentence also carries a TEXT_SURFACE term
# ("the phone screen shows … 'Tenant Complaint Pending'"), never on a bare quoted name
# ("a model showing the 'Aster Meridian 38' on her wrist").
DISPLAY_VERBS = ("displays", "displaying", "showing", "shows")
# K-06: a numeral/digit term is the watch's own dial furniture, not requested text, when one
# of these qualifies it ("Arabic numerals at 12, 3, 6 and 9", "the date digits at 3 o'clock",
# "Roman numerals, no other markings"). Fixed-width lookbehinds, one per qualifier.
DIAL_NUMERAL_QUALIFIERS = ("arabic", "roman", "hour", "date", "dial", "applied", "luminous",
                           "minute", "index")
NOT_AFTER_DIAL_QUALIFIER = "".join(rf"(?<!{q}\s)" for q in DIAL_NUMERAL_QUALIFIERS)
# T2 (b): a request for rendered text.
TEXT_REQUEST_TERMS = (
    "captions?", "subtitles?", "headlines?", "taglines?", r"title\s+cards?", "typography",
    "lettering", "wordmarks?", "logos?", r"on-screen\s+text", r"text\s+overlays?", "watermarks?",
    r"text\s+reading", r"label\s+reading",
    # F-03 additions
    r"text\s+(?:on|across|along|over|around|at|in|above|below|beneath|under|near)\b",
    r"(?:add|adds|adding|place|placed|placing|render|rendered|rendering|include|includes|"
    r"including|put|print|printed|printing|write|set|with|featuring|feature|features|bearing|"
    r"bears|carrying|carries)\s+(?:\w+\s+){0,2}?text(?!-free)\b",
    r"the\s+words?\b", "letters", r"spell(?:s|ed|ing)?\s+out",
    # K-06: not the watch category's own dial vocabulary ("Arabic numerals", "date digits")
    NOT_AFTER_DIAL_QUALIFIER + "numerals?", NOT_AFTER_DIAL_QUALIFIER + "digits",
    r"(?:model|brand|product|company|shop|store|business)\s+names?",
    r"(?:owner|manager|tenant|customer|founder)(?:'s)?\s+names?",
    r"bearing\s+(?:\w+(?:'s)?\s+){0,4}names?\b",
    r"engraved\s+with", "engravings?", "inscriptions?", "inscribed",
    r"(?:that|which)\s+(?:says|reads)\b",
    r"(?:phone|mobile|whatsapp|contact)\s+numbers?", "helpline",
    "urls?", r"web(?:site)?\s+address(?:es)?", r"www\.", r"[\w-]+\.(?:com|in|co|ai|org|net|io)",
    r"https?://", "written", "hand-written", "handwriting", "slogans?", "mottos?",
    "straplines?", "devanagari", "cta", r"call[- ]to[- ]action", r"body\s+copy", r"text\s+links?",
    r"text\s+labels?",
    r"[\"'“‘][^\"'”’\n]{2,40}[\"'”’]\s+(?:button|tab|link|chip|badge|label|banner|toggle)",
)
# A negator within 4 tokens before a T2 / T3 term clears it.
NEGATORS = ("no", "not", "never", "without", "avoid", "zero")
NEGATOR_PHRASES = ("rather than", "never a", "free of", "devoid of", "absence of")
# T3 only (K-03): the negator governs the surface term only when the gap between them holds
# no punctuation, no gerund (-ing) and none of these words — otherwise it governs something
# else ("Avoid cluttering the dashboard", "zero clutter around the invoice") and the surface
# is still drawn.
GOVERNANCE_BREAK = r"[,;:()\[\]—–]"
GOVERNANCE_STOP_WORDS = frozenset((
    "around", "on", "in", "of", "at", "over", "under", "near", "beside", "behind", "across",
    "with", "from", "to", "into", "onto", "for", "by", "through", "against", "and", "but", "or",
))
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
# T3: a text-bearing surface with no illegibility/deferral term in the same sentence and no
# NEGATOR within 4 tokens before it. Bare chat/conversation/message/counter/menu/button/
# banner/interface were narrowed to qualified forms (F-02).
TEXT_SURFACE_TERMS = (
    r"chat\s+bubbles?", r"chat\s+threads?", r"chat\s+(?:window|screen|messages?|list|app)",
    r"whatsapp\s+(?:chats?|conversations?|messages?|threads?)",
    r"text\s+(?:conversations?|messages?|threads?)", r"message\s+(?:bubbles?|threads?|list)",
    r"unread\s+messages?", "notifications?", "badges?",
    r"(?:notification|unread|badge)\s+counter", "spreadsheet", "excel", r"#REF", "ledger",
    "notebook", "handwritten", r"signs?(?!\s+of\b)", "signage", "signboards?", "chart", "poster",
    "receipt", "invoice", r"price\s+tag", r"restaurant\s+menu", r"menu\s+(?:board|card)",
    r"printed\s+menu", r"(?:app|dropdown)\s+menu", "newspaper", "dashboard", r"app\s+icon",
    r"app\s+screen", r"home\s+screen", "UI", r"(?:app|user|mobile|software)\s+interface",
    r"(?:cta|app|download|on-screen|ui)\s+buttons?", r"buttons?\s+(?:labell?ed|reading|text)",
    r"(?:shop|ad|web|promotional|vinyl|advertising|street|notification)\s+banners?",
    r"banner\s+(?:ads?|text)", r"phone\s+screens?", r"smartphone\s+screens?",
    r"laptop\s+screens?", r"screen\s+showing", r"screen\s+shows", r"screen\s+filling",
    r"screens\s+showing",
    # F-03 additions; K-06: `label-free`/`label-less` is the absence of one, and a storefront
    # names a surface only with its sign/lettering/name/board
    r"labels?(?!-free)(?!-less)", "placards?", "calendars?",
    r"(?:licen[cs]e|number|registration)\s+plates?",
    "nameplates?", r"name\s+(?:plates?|boards?)", "billboards?", "hoardings?",
    r"storefronts?\s+(?:signs?|signage|signboards?|lettering|names?|text|boards?)",
)
ILLEGIBILITY_TERMS = (
    "illegible", "unreadable", "blurred", r"out\s+of\s+focus", "blank", r"dark\s+screen",
    r"switched\s+off", r"screen\s+replacement", r"replaced\s+in\s+post", r"green\s+screen",
    "greenscreen", "placeholder", r"no\s+legible", r"no\s+readable", r"added\s+in\s+post",
    "composited",
    # F-02 additions
    r"not\s+visible", r"screen\s+off", r"screens?\s+(?:are\s+|is\s+)?(?:off|dark|black)\b",
    r"powered\s+off", r"turned\s+off", "off-screen", "invisible",
)
# Detail line only (no status effect): does the prompt carry an explicit no-text clause?
NO_TEXT_CLAUSE = (
    r"\bno\b[^.;,\n]{0,24}?\b(?:text|lettering|typography|captions?|logos?|watermarks?|words)\b"
    r"|\btext[- ]free\b"
)
