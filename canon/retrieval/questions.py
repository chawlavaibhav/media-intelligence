"""The production-question catalogue: what a media job needs to KNOW, not who can make it.

EVAL-037 searched the customer's words. The Sonnet CONTROLLED_CANON lane shows what that
costs even when it works: three searches per trial, each a hand-written paraphrase of the
brief, with the model itself writing out its knowledge needs first ("How to light/style a
beverage product shot ... to read as premium rather than cheap soda"). Those declared needs
are the retrieval plan. The model was doing the planning step by hand, in prose, every
time, and no two repetitions of the same brief planned identically.

This module makes that step explicit and repeatable. A production question names a
knowledge need in the customer's outcome — composition, lighting, legibility, message
structure, shot grammar, persuasion, brand, cultural context, failure prevention — and
carries the vocabulary that finds it in Canon.

**Boundary, stated because it is easy to erode:** a production question asks what must be
understood to specify the work. It never asks which image or video model to use, what a
provider charges, or whether a model can execute something reliably. That is capability
routing, it is the Eval stream's and the (still empty) Capability Registry's question, and
`coordination/PROJECT-CONTRACT.md` keeps the two apart. Nothing in this catalogue names a
model, a provider or a price, and the test suite asserts that.

`cue_terms` are matched against the customer's request text on WORD boundaries, not as
substrings. That distinction is not pedantry: an earlier substring version fired the
lighting question on the word "dialogue", because "dialogue" contains "dial". A
deterministic, inspectable rule beats a clever one nobody can reproduce — but it has to be
the right rule.

`expansion_terms` are what the question actually searches Canon with — the domain
vocabulary the books use, which is often not the vocabulary a customer uses.
"""
import re

_WORD_RE = re.compile(r"[a-z0-9]+")


def normalise(text):
    """Lowercase word stream, space-delimited at both ends, for boundary-safe matching."""
    return " " + " ".join(_WORD_RE.findall((text or "").lower())) + " "


def contains_cue(normalised_text, cue):
    """True when `cue` appears in the text as a whole word or whole phrase."""
    return f" {' '.join(_WORD_RE.findall(cue.lower()))} " in normalised_text

MEDIA_IMAGE = "image"
MEDIA_VIDEO = "video"
MEDIA_UNSPECIFIED = "unspecified"

# Deterministic media detection. Only cues that are unambiguous in a brief are listed.
_VIDEO_CUES = ("video", "film", "reel", "seconds", "duration", "9 16", "16 9",
               "shot", "shots", "scene", "cut", "cuts", "footage", "ad film", "spot",
               "storyboard", "voiceover", "dialogue", "ugc")
_IMAGE_CUES = ("image", "poster", "still", "photograph", "photo", "4 5", "1 1",
               "hero image", "banner", "key visual", "packshot")


class ProductionQuestion:
    """One knowledge need, its search vocabulary, and how it allocates its slots."""

    __slots__ = ("qid", "plain_english", "cue_terms", "expansion_terms", "media",
                 "base_for", "kind_sequence")

    def __init__(self, qid, plain_english, cue_terms, expansion_terms,
                 media=("image", "video", "unspecified"), base_for=(), kind_sequence=None):
        self.qid = qid
        self.plain_english = plain_english
        self.cue_terms = tuple(cue_terms)
        self.expansion_terms = tuple(expansion_terms)
        self.media = tuple(media)
        self.base_for = tuple(base_for)
        # Only set where this question genuinely wants a different mix from the default;
        # otherwise `rank.DEFAULT_KIND_SEQUENCE` applies.
        self.kind_sequence = kind_sequence

    def query_text(self, request_terms=()):
        """The text this question searches Canon with: its own vocabulary plus any
        request words that triggered it. The raw request is never searched wholesale."""
        return " ".join(list(self.expansion_terms) + list(request_terms))

    def as_dict(self):
        return {"question_id": self.qid, "plain_english": self.plain_english,
                "expansion_terms": list(self.expansion_terms)}


CATALOGUE = [
    ProductionQuestion(
        "composition_hierarchy",
        "How should the frame be composed, and what must the viewer notice first?",
        cue_terms=("hero", "layout", "composition", "hierarchy", "poster", "frame",
                   "typography", "clean", "premium", "minimal", "grid", "space"),
        expansion_terms=("composition", "visual hierarchy", "focal point", "dominance",
                         "framing", "placement", "eye movement", "attention", "balance",
                         "negative space", "grid", "scale", "contrast", "emphasis"),
        base_for=(MEDIA_IMAGE, MEDIA_UNSPECIFIED),
    ),
    ProductionQuestion(
        "lighting_material",
        "How should light and material be handled so surfaces read the way they should?",
        cue_terms=("light", "lighting", "metal", "steel", "glass", "sapphire", "gloss",
                   "shine", "reflection", "texture", "material", "condensation", "shadow",
                   "skin", "leather", "matte", "dial", "surface", "sunburst"),
        expansion_terms=("lighting", "reflection", "family of angles", "specular",
                         "direct reflection", "diffuse", "highlight", "shadow", "contrast",
                         "surface", "texture", "material", "gloss", "key light", "fill"),
        # Lighting and material is where a figure most often carries the argument the
        # prose does not, so visual evidence is promoted ahead of the second claim.
        kind_sequence=("knowledge", "visual_evidence", "concept_system", "knowledge",
                       "binding", "ontology_concept", "ontology_term"),
    ),
    ProductionQuestion(
        "product_legibility",
        "How is the product kept legible, accurate and unmistakably the subject?",
        # "price" and "pricing" here mean a price PRINTED IN THE CREATIVE that has to be
        # readable — the festive-poster brief turns on it. They are never about what a
        # provider charges us, which is not a Canon question at all.
        cue_terms=("product", "packshot", "sku", "hero", "label", "packaging", "geometry",
                   "detail", "accurate", "legible", "readable", "price", "pricing", "text"),
        expansion_terms=("product", "subject", "legibility", "clarity", "detail",
                         "recognition", "identification", "distortion", "accuracy",
                         "reading", "figure ground", "isolation"),
    ),
    ProductionQuestion(
        "message_structure",
        "How should the advertising message be structured so the point lands?",
        cue_terms=("ad", "advertising", "campaign", "message", "proposition", "offer",
                   "cta", "sell", "commercial", "promotional", "headline", "claim",
                   "benefit", "performance", "conversion", "purchase"),
        expansion_terms=("advertising", "message", "proposition", "headline", "copy",
                         "claim", "benefit", "offer", "call to action", "clarity",
                         "single message", "promise", "reason to believe", "selling"),
        base_for=(MEDIA_UNSPECIFIED,),
    ),
    ProductionQuestion(
        "shot_grammar",
        "How should shots be chosen, ordered and cut so the scene reads correctly?",
        cue_terms=("shot", "shots", "scene", "cut", "edit", "sequence", "continuity",
                   "coverage", "dialogue", "camera", "pacing", "duration", "video",
                   "storyboard", "reverse", "eyeline"),
        expansion_terms=("shot", "cut", "editing", "continuity", "screen direction",
                         "axis of action", "coverage", "shot size", "sequence", "rhythm",
                         "pacing", "transition", "eye line", "camera movement"),
        media=(MEDIA_VIDEO, MEDIA_UNSPECIFIED),
        base_for=(MEDIA_VIDEO,),
    ),
    ProductionQuestion(
        "persuasion_memory",
        "What makes this communication persuasive and memorable rather than merely seen?",
        cue_terms=("persuade", "memorable", "emotional", "story", "credible", "trust",
                   "attention", "recall", "engaging", "authentic", "believable", "hook"),
        expansion_terms=("persuasion", "memory", "attention", "emotion", "story",
                         "concrete", "unexpected", "credibility", "simplicity",
                         "recall", "salience", "distinctiveness", "engagement"),
    ),
    ProductionQuestion(
        "brand_handling",
        "How should the brand's own assets, colours and voice be handled?",
        cue_terms=("brand", "logo", "wordmark", "identity", "palette", "colour", "color",
                   "tone of voice", "consistency", "guidelines", "website"),
        expansion_terms=("brand", "identity", "logo", "consistency", "palette", "colour",
                         "typography", "tone", "recognition", "distinctive asset",
                         "coherence"),
    ),
    ProductionQuestion(
        "cultural_communication",
        "What does this specific cultural audience context require, and what would ring false?",
        cue_terms=("india", "indian", "festive", "diwali", "hindi", "hinglish", "vernacular",
                   "regional", "local", "cultural", "culturally", "cliche", "cliché",
                   "authentic", "urban", "desi", "bharat"),
        expansion_terms=("india", "indian", "culture", "cultural", "vernacular", "local",
                         "consumer", "market", "audience", "idiom", "familiarity",
                         "aspiration", "everyday", "context"),
    ),
    ProductionQuestion(
        "failure_prevention",
        "What commonly goes wrong in work like this, and what does the source say to inspect?",
        # Deliberately no bare "not" or "without": they appear in almost every brief and
        # would make this question's cue count meaningless. It is a base question anyway.
        cue_terms=("avoid", "cheap", "generic", "cliche", "cliché", "wrong", "fail",
                   "mistake", "problem", "risk", "must not", "never"),
        expansion_terms=("failure", "problem", "mistake", "avoid", "confusion", "unclear",
                         "distraction", "inconsistent", "breaks", "defect", "weak",
                         "remedy", "correction", "check"),
        base_for=(MEDIA_IMAGE, MEDIA_VIDEO, MEDIA_UNSPECIFIED),
        # What goes wrong lives in the source's own problem vocabulary and in the
        # bindings that diagnose or flag, so both come early here.
        kind_sequence=("knowledge", "binding", "ontology_term", "knowledge",
                       "concept_system", "ontology_concept", "visual_evidence"),
    ),
]

BY_ID = {q.qid: q for q in CATALOGUE}
QUESTION_IDS = tuple(q.qid for q in CATALOGUE)


def detect_media(request_text):
    """image / video / unspecified, from unambiguous cues only.

    Ties go to `unspecified` rather than to a guess: an unspecified plan is a wider,
    honest plan, and a wrong guess silently drops the right question.
    """
    text = normalise(request_text)
    video = sum(1 for cue in _VIDEO_CUES if contains_cue(text, cue))
    image = sum(1 for cue in _IMAGE_CUES if contains_cue(text, cue))
    if video > image:
        return MEDIA_VIDEO
    if image > video:
        return MEDIA_IMAGE
    return MEDIA_UNSPECIFIED
