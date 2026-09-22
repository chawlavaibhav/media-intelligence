You are the creative director on a media-agency job. Produce the Stage 3 creative board for the brief below, as ONE JSON object written to the output path given at the end. No other files. Do not read any repository file, and do not search for anything: everything you may use is in this prompt.

The board must have exactly these fields (this is the shape the agency's gate validates):
- "proposition": one sentence.
- "board": {"kind": "film", "duration_s": <number>, "style_line": <fixed opening line of every prompt>, "negative_line": <fixed closing line: no text, no logos…>, "identity_anchors": {<name>: <verbatim description restated in every prompt>, …}, "hero_frame": {"beat": <n>, "description": <the one frame that sells the product without copy — a frame, never a claim>}, "audio": {"native_audio": <bool>, "music_bed": <string>, "voice_over": <string or "none">}, "beats": [ {"n": 1, "t_in": 0, "t_out": …, "clip_s": …, "title": …, "feeling": <what the viewer feels>, "framing": <what is in the frame, where, what moves>, "first_frame": <what the STILL shows at t_in, before anything moves>, "impact": <how the beat lands: camera, hold, sound, performance>, "canon": [<ids of any supplied knowledge you applied here, or empty>], "mandatory_ids": [<which brief requirements this beat carries, as M1, M2… of your own numbering>]}, … ] } — beats contiguous, t_out of the last = duration_s; the last beat may be a code-composed brand close (clip_s 0).
- "copy_deck": {"strings": {<id>: <exact on-screen text>}, "sources": {<id>: <where each string comes from>}, "placements": {<name>: {"t_in":…, "t_out":…, "contents": [<string ids>], "why": …}}}.
- "mandatory": [{"id": "M1", "customer_words": <the brief's own words>, "realisation": <how the film carries it>}, …] — every requirement in the brief.
- "brand_timeline": {"first_mark_s": …, "in_context": …, "spoken": …}, "ask": {"string_id": …, "surface": "card"|"super", "at_s": …}, "last_frame": …, "muted_test": "yes"|"no".
- "deviations": [{"from": <a supplied default you overrode>, "brief_clause": <the customer clause that forces it>}] — may be empty.
- "knowledge_used": [{"id": <id>, "used_for": <beat or decision>}] — every supplied knowledge item you actually applied; empty if none supplied or none used. Never invent an id.

Constraints that always apply: everything is produced by generative models (a still per beat, then image-to-video per beat, stitched by code; exact text composed by code, never generated); no dialogue or voice-over; no named film, actor, character or copyrighted work; the product must be a recognisable likeness of the real one; 9:16, 15–30 s.

Write the best board you can. Quality is judged by a non-author on: whether the hero frame sells without copy; how specific and producible each beat's feeling / framing / first_frame / impact are; whether every brief requirement lands on a beat; brand timing; and honesty (a deviation is declared, not hidden).

## THE BRIEF (verbatim job record)
{
 "brief": {
  "language": "en",
  "market": "IN",
  "text": "lets make an ad with mokobara. i would preferably give it the odysey movie angel. the proatagonist had mokbara bags. the protagonist found his mokobara bag, while he was on the island where he was kept for years. in that bag he founds her wives photo and a lot of stuff that he could use to go back. he packs food and stuff and goes back. would be funny that he could keep his arms in the bag and food and so much stuff. Avoid getting copyright violoations from odysssey."
 },
 "customer_ref": "acct-mokobara-spec",
 "deliverable_request": {
  "aspect": "9:16",
  "count": 1,
  "kind": "multi_shot_story",
  "modality": "video",
  "motion": {
   "audio": true,
   "from": "generated",
   "seconds": 30
  },
  "operation": "generate",
  "subject": {
   "entity": "product",
   "entity_id": "mokobara_transit_backpack_private_island",
   "identity_invariants": [
    "deep navy matte body",
    "bright yellow lining",
    "vertical front zip and front bucket pocket with two black zip pulls",
    "black padded straps, small top grab handle"
   ]
  }
 },
 "exact_text_strings": [
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "Transit Backpack"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "30L"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "mokobara.com"
  }
 ],
 "reference_assets": [
  {
   "asset_id": "mokobara_wordmark",
   "content_type": "image/svg+xml",
   "depicts_identifiable_person": false,
   "provenance": "customer_site",
   "role": "logo",
   "sha256": "c443658f13bed93aa1adbb6bcbc5fcbb06fc4d9abdafd0f59f5da593c67356eb"
  },
  {
   "asset_id": "transit_backpack_private_island_1",
   "content_type": "image/jpeg",
   "depicts_identifiable_person": false,
   "provenance": "customer_site",
   "role": "product",
   "sha256": "689aca0e7a548b43cf509dd2966f9d134c3c85108ad15dfee88c98649adeda46"
  }
 ],
 "job_id": "AGY-2026-09-21-MOKOBARA-ODYSSEY-001",
 "policy_profile": "dry",
 "retention": {
  "policy_ref": "alpha-1-default"
 },
 "submitted_by": "producer-mokobara"
}
## SUPPLIED KNOWLEDGE — accepted claims from the agency's library (apply what fits; cite the sk_ ids in `canon` / `knowledge_used`)
### sk_abcd_0007  (google-abcd-video-ads)  label: open_in_the_middle_of_the_action_or_on_a_close_up
claim_type: explicit_source_claim  ·  scope: ['youtube_video_advertising', 'shot_design', 'short_form_video_advertising']  ·  conditions: Offered at the storyboard stage of an ad whose concept is already approved
claim: The source names two concrete opening constructions for an ad — beginning in the middle of the action, and opening on a close-up — and offers bold imagery at the start as a third means. It presents them as examples of many possible ways to earn engagement immediately, not as a required opening.
source_terms: You can start your ad in the middle of the action, or open with a close-up | Play around with bold imagery at the start of your ad to create an attention-grabbing opening | Start big!
source_stated_remedies: Start your ad in the middle of the action, or open with a close-up
caveats: The source hedges explicitly — "there are many ways to do this" — so these are illustrations of a principle, not a closed list and not [...] | This appears only on the Think with Google page. The Google Ads Help core table names no opening construction at all; it stops at "Jump in". | Platform- and time-contingent. This is guidance about one company's ad products on one platform. Playback behaviour, ad formats and [...]

### sk_abcd_0010  (google-abcd-video-ads)  label: branding_early_often_and_richly
claim_type: explicit_source_claim  ·  scope: ['youtube_video_advertising', 'brand_communication']  ·  conditions: YouTube video ads; the 'telling' half assumes audio is heard
claim: The source's branding principle has three separate dimensions in one line: when the brand first appears (early), how often it recurs (often), and how many different kinds of branding element carry it (richly). The third is the one that distinguishes this from a simple frequency instruction — the source asks for variety of asset, not just repetition.
source_terms: Brand early, often, and richly | Make use of a broad range of branding elements to show and tell viewers who you are
source_stated_remedies: Brand early, often, and richly
caveats: "Early", "often" and "richly" are all unquantified. No timing, no count and no minimum number of asset types is given anywhere in the [...] | Platform- and time-contingent. This is guidance about one company's ad products on one platform. Playback behaviour, ad formats and [...] | Declared publisher interest. The publisher sells advertising on the platform whose creative guidance this is, and the cited research [...]

### sk_abcd_0011  (google-abcd-video-ads)  label: brand_shows_up_early_and_throughout
claim_type: explicit_source_claim  ·  scope: ['youtube_video_advertising', 'brand_communication']  ·  conditions: A core Branding guideline, before any objective-specific tailoring
claim: The brand or the product is to be introduced from the start of the ad and its presence maintained across the ad's whole length. The source treats these as one instruction: an early appearance that then lapses does not satisfy it.
source_terms: Show up early and throughout | Introduce your brand or product from the start and maintain that presence
source_stated_remedies: Introduce your brand or product from the start and maintain that presence
caveats: The source's own worked example names a window — "Weekendesk introduces its brand in the first 5s" — but that figure describes one ad [...] | The instruction permits either the brand or the product to carry the early presence; the source does not say which is preferable in [...] | Platform- and time-contingent. This is guidance about one company's ad products on one platform. Playback behaviour, ad formats and [...]
GUARD relations (closure must cite, conflict-list or waive each partner): qualified_by → sk_abcd_0026 (the full-funnel row reshapes what appears early and what appears late)

### sk_abcd_0012  (google-abcd-video-ads)  label: see_and_say_audio_brand_mention_reinforces_onscreen_branding
claim_type: explicit_source_claim  ·  scope: ['youtube_video_advertising', 'brand_communication']  ·  conditions: YouTube, where the source states audio is almost always heard
claim: The source claims an interaction rather than an addition: an audio mention of the brand raises the performance of the on-screen brand visual it accompanies. The instruction is to pair the two, not to choose between them.
source_terms: See and say | Reinforce with audio | Audio brand mentions enhance onscreen brand visuals' performance | Supercharge your brand visual performance with audio brand mentions
source_stated_remedies: Supercharge your brand visual performance with audio brand mentions
caveats: "Enhance ... performance" is a performance claim with no figure, no measure and no study attached at this level. The named study [...] | The claim depends on the audio actually being heard, which the source asserts for YouTube specifically. On a surface where audio is [...] | Platform- and time-contingent. This is guidance about one company's ad products on one platform. Playback behaviour, ad formats and [...]
GUARD relations (closure must cite, conflict-list or waive each partner): depends_on → sk_abcd_0014 (the claim assumes the audio is heard)

### sk_alt_c003_0018  (alton-painting-with-light-ch2)  label: genre_sets_the_key_of_the_whole_picture_before_any_scene_is_lit
claim_type: explicit_source_claim  ·  scope: ['cinematography', 'genre']  ·  conditions: a whole production, decided before scene work
claim: Before scenes are worked out, a decision is made at the level of the whole film. The source names three categories from the point of view of illumination — comedy, subdivided into musical and slapstick; drama; and mystery — each requiring a different approach. Once the key of the picture is decided, the script is broken down into sequences and scenes and each mood is worked out separately. For musical comedy, the source states that light sources and logic in lighting mean nothing; comedy is lit as high as the stock and laboratory allow without becoming senselessly flat, because a low-key scene would spoil the comic effect.
source_terms: The key of the picture (not to be confused with keylight) depends upon the category of the screen play. | Musical comedies are lit high and brilliant with a stylized, dreamlike light. For this type of photography, light sources and logic in lighting mean nothing.
source_stated_problems: a low-key scene might be upsetting and spoil the comedy effect
source_stated_remedies: decide the key of the picture first, then break the script down
caveats: the source explicitly warns that the key of the picture is not the keylight, which is the one place in the chapter it guards against [...] | the three genre categories are the studio system's commercial categories of the period, not a general taxonomy | the musical-comedy exemption from source logic sits directly against the chapter's own rule that the key must appear to come from an [...]
GUARD relations (closure must cite, conflict-list or waive each partner): contradicts → sk_alt_c003_0011 (musical comedy is exempted from the requirement that lighting agree with an [...])

### sk_fre_c003_0025  (freeman-photographers-eye-graphic-guide)  label: a_still_reveal_is_a_balancing_act_between_delay_and_abandonment
claim_type: explicit_source_claim  ·  scope: ['photography', 'cinema']  ·  conditions: a still image with a secondary subject intended to be found late
claim: The reveal is a cinematic device — the camera shows one thing, then moves or zooms to disclose something else, effective through surprise — and the source says it is difficult and perhaps impossible to achieve in a single still. The only approach is to arrange framing, composition or lighting so that attention goes immediately to one place, but the eye lingers long enough to start wandering and then discovers something else. It is an uncertain balancing act: hide the thing to be revealed too well — too small, too poorly lit — and the viewer will get bored and move on before noticing it.
source_terms: The only way to come close to this in a still image is to arrange the framing, composition or lighting so that all the attention immediately goes to one [...] | It’s an uncertain balancing act, because if you hide the thing-to-be-revealed too well, such as by making it too small or poorly lit, chances are the [...]
source_stated_problems: hiding the thing-to-be-revealed so well the viewer moves on before noticing it
source_stated_remedies: arrange framing, composition or lighting so attention goes to one place and then wanders
caveats: the source states the technique may be impossible in a still and then attempts it anyway — "But let's try anyway" — so the case is [...] | success and failure are described only in terms of the viewer's patience, and no way of testing whether the balance was struck is given
GUARD relations (closure must cite, conflict-list or waive each partner): depends_on → sk_fre_c003_0024 (requires a small element to remain findable)

### sk_gos_c003_0007  (grammar-of-the-shot-ch4)  label: screen_direction_must_be_maintained_across_a_cut
claim_type: explicit_source_claim  ·  scope: ['motion_picture_production']  ·  conditions: a subject moving left or right across consecutive shots
claim: A subject's left or right movement must be maintained from one shot to the next. A person who exits frame left must enter the following shot from frame right, because within the film's space their leftward journey is understood to continue until something on screen shows it change.
source_terms: screen direction—the left or right movement of a subject—must be maintained from one shot to the next | if a person walks out of frame left ... in this new shot they would have to be entering from frame right in order to maintain that direction of leftward [...]
source_stated_remedies: have the subject enter the new shot from the edge opposite the one they exited
caveats: the rule holds until a change of movement is shown on screen, so it governs the unseen interval rather than the whole film
GUARD relations (closure must cite, conflict-list or waive each partner): depends_on → sk_gos_c003_0005 (defined relative to the frame edges); contradicts → sk_gos_c003_0012 (jumping the line is the failure of this rule)

### sk_gote_c003_0004  (grammar-of-the-edit-ch3-5)  label: every_new_shot_must_carry_new_information
claim_type: explicit_source_claim  ·  scope: ['film_editing', 'television_editing']  ·  conditions: every transition
claim: Each shot cut to must give the viewer information it did not already have. The information may be visual — a character entering, a new location, an unexplained event — or aural, such as narration or an off-screen sound. The source states this is basic to all editing choices, and frames the editor's working question as: what would, should, cannot and do I wish the audience to see next.
source_terms: A new shot should always present some new information to the viewer. | this element of new information is basic to all editing choices
source_stated_problems: the audience notices the physical act of the edit
source_stated_remedies: give the new shot something the audience does not yet have
caveats: the information may be deliberately misleading; the source cites showing false information in a mystery, and showing the audience what [...] | no test is offered for how much novelty counts as new information, so the rule is applied by judgement
GUARD relations (closure must cite, conflict-list or waive each partner): qualified_by → sk_gote_c003_0006 (information governs the shot cut to; motivation governs the shot cut from)

### sk_gote_c003_0006  (grammar-of-the-edit-ch3-5)  label: every_departure_from_a_shot_must_be_motivated
claim_type: explicit_source_claim  ·  scope: ['film_editing', 'television_editing']  ·  conditions: every transition
claim: Information governs the shot being cut to; motivation governs the shot being cut away from. There must always be a reason to leave the current shot and a reason it is left at that particular moment. The motivating element may be visual — usually some movement by a subject or object, from a car clearing a river down to a small shift of a character's eyes — or aural.
source_terms: There should always be a motivation for making a transition away from a shot. | This motivation can be either visual or aural.
source_stated_problems: there is no reason to leave the shot at that moment
source_stated_remedies: find the movement or sound in the outgoing shot that creates the need to see the next one
caveats: the source's worked example — a man's eyes move left, cut to the cat he is looking at — is not what the accompanying figure depicts; [...]
GUARD relations (closure must cite, conflict-list or waive each partner): qualifies → sk_gote_c003_0004 (the two factors govern opposite ends of the same transition)

### sk_hea_mts_0011  (heath-made-to-stick-introduction)  label: grabbing_attention_and_holding_interest_are_different_problems
claim_type: explicit_source_claim  ·  scope: ['communication', 'teaching']  ·  conditions: ideas that take time to deliver
claim: Getting attention and keeping it are two problems needing two devices. Surprise seizes attention but decays, so an idea that must be delivered over time requires curiosity instead, generated by systematically opening gaps in what the audience knows and then filling them. The source's test case is holding students through the forty-eighth history class of the year.
source_terms: But surprise doesn't last. For our idea to endure, we must generate interest and curiosity. | We can engage people's curiosity over a long period of time by systematically "opening gaps" in their knowledge—and then filling those gaps.
source_stated_problems: But surprise doesn't last.
source_stated_remedies: systematically "opening gaps" in their knowledge—and then filling those gaps
caveats: Recorded separately from the unexpectedness principle because it names a different problem, supplies a different device and a [...]

### sk_hop_sa_0026  (hopkins-scientific-advertising-ch1-7)  label: a_picture_must_earn_the_space_it_occupies
claim_type: explicit_source_claim  ·  scope: ['mail_order_advertising', 'advertising']  ·  conditions: direct-reply advertising for a practical, considered purchase
claim: A picture in an advertisement must be a salesman in itself and earn the space it occupies, with its size gauged by its importance to the sale. Pictures used to decorate or merely to interest are waste. The source reports a mail order incubator advertiser whose type advertisements with the right headlines already brought excellent returns, and who added a row of chickens in silhouette at 50 per cent more space: the advertisement was more striking, cost per reply rose by exactly 50 per cent, and it brought not one added sale. The lesson drawn is that incubator buyers were practical people looking for attractive offers, not for pictures.
source_terms: In mail order advertising the pictures are always to the point. They are salesmen in themselves. They earn the space they occupy. | So he increased his space 50 per cent to add a row of chickens in silhouette. It did make a striking ad, but his cost per reply was increased by exactly [...] | Before you use useless pictures, merely to decorate or interest, look over some mail order ads.
source_stated_problems: useless pictures, merely to decorate or interest | Pictures in ordinary advertising may teach little. They probably result from whims.
source_stated_remedies: They earn the space they occupy. The size is gauged by their importance.
caveats: The most nearly controlled comparison in the section: one variable added to an existing advertisement, with a reported result on both [...] | The source draws a general rule about decorative pictures from a case whose own explanation is specific to the buyers of that product, [...]
GUARD relations (closure must cite, conflict-list or waive each partner): depends_on → sk_hop_sa_0021 (presented as one of the things mail order teaches)

### sk_mla_0064  (hopkins-my-life-in-advertising)  label: amusement_buys_attention_from_the_wrong_people
claim_type: explicit_source_claim  ·  scope: ['advertising', 'persuasion', 'copywriting']  ·  conditions: all advertising except advertising for amusements, which the source exempts
claim: The source rules out humour and frivolity, and separately rules out competing with editorial matter. On humour its argument is that spending money is serious business — money represents life and work, spending in one direction means skimping in another, and the average person is constantly choosing between ways to spend — so an appeal for money made in a light-some way will not get it. It exempts amusement advertising explicitly and says the rule applies to all other forms. On competing with editorial its argument is about the composition rather than the volume of attention: an advertisement built to rival the stories, news, pictures or cartoons may win attention but not valuable attention, because most of the people it attracts have no interest in the subject. It adds that any product worth advertising, rightly presented, has more interest than a story to the people who want it, and asks why a lasting appeal should be traded for a moment of fickle attention.
source_terms: Frivolity has no place in advertising. Nor has humor. | Nobody can cite a permanent success built on frivolity. People do not buy from clowns. | Never seek to amuse. That is not the purpose of advertising. People get their amusements in the reading-matter columns. | You may win attention, but not valuable attention.
source_stated_problems: What does it profit an advertiser to attract a reader who has no interest in his subject?
source_stated_remedies: The only interest you can offer profitably is something people want.
caveats: The evidence is that the source cannot cite a permanent success built on frivolity and names two campaigns of its era it says proved [...] | The source's own doctrine that curiosity is the strongest activating factor (sk_mla_0010), and its own delight in a phrase peers [...] | Culturally and historically bounded. This is a claim about how a particular public in a particular period related to money and to print.
GUARD relations (closure must cite, conflict-list or waive each partner): trades_off_with → sk_mla_0010 (curiosity is endorsed while amusement is refused, on the ground of who is attracted)

### sk_murch_c003_0020  (murch-blink-p1-25)  label: emotion_ranks_first_and_is_worth_more_than_the_other_five_combined
claim_type: explicit_source_claim  ·  scope: ['film_editing']  ·  conditions: any cut in a narrative film
claim: Emotion is the first criterion, weighted by the source at 51 percent — more than the other five combined. A cut should be true to the emotion of the moment, and emotion should be preserved at all costs. The source states it is the thing film school comes to last, if at all, because it is the hardest to define and deal with, and that what an audience finally remembers is not the editing, the camerawork, the performances or even the story, but how they felt.
source_terms: 1) Emotion 51% | it is true to the emotion of the moment | Emotion, at the top of the list, is the thing that you should try to preserve at all costs. | What they finally remember is not the editing, not the camerawork, not the performances, not even the story-it's how they felt.
caveats: the source's working question is "How do you want the audience to feel?", set in italics on the page — the criterion is a question to [...] | 51 percent is not an arbitrary number: it is the smallest whole percentage constituting a majority, so the weight is a way of saying [...] | the highest-weighted criterion in the framework is also the one the source says is hardest to define, which means the list is anchored [...]

### sk_ogl_c003_0014  (ogilvy-ch2-advertising-that-sells)  label: make_the_product_the_hero
claim_type: explicit_source_claim  ·  scope: ['advertising']  ·  conditions: wherever possible, per the source
claim: The product itself should be made the hero of the advertising wherever possible. The source rejects the excuse that a product is too dull, holding that there are no dull products only dull writers, and reports never assigning a product to a writer not personally interested in it, because every bad campaign the author wrote was for a product that did not interest him.
source_terms: Whenever you can, make the product itself the hero of your advertising. | there are no dull products, only dull writers
source_stated_remedies: make the product itself the hero | do not assign a product to a writer who is not interested in it
caveats: the source notes that showing the product with utter simplicity takes courage, because the writer will be accused of not being creative
GUARD relations (closure must cite, conflict-list or waive each partner): contradicts → sk_ogl_c003_0020 (the source sets this against the cult of creativity)

### sk_ogx_0032  (ogilvy-beyond-ch2)  label: humour_now_sells_a_reversal_the_author_dates_and_attributes_to_new_measurement
claim_type: explicit_source_claim  ·  scope: ['television_advertising']  ·  conditions: television commercials measured for change in brand preference, at the time of writing
claim: The source reverses a position he had held and states when and why. Conventional wisdom, and Hopkins, held that people do not buy from clowns; he believed this was true in Hopkins's day and until recently, and says the latest wave of factor analysis reveals that humour can now sell. He adds that this came as a relief because he had disliked himself for rejecting funny commercials, and immediately bounds the reversal: very few writers can write funny commercials that are funny, and anyone who is not one of them should not try.
source_terms: Claude Hopkins, the father of modern advertising, thundered, 'People don't buy from clowns' | I think this was true in Hopkins' day, and I have reason to believe that it remained true until recently, but the latest wave of factor-analysis reveals [...] | very, very few writers can write funny commercials which are funny. Unless you are one of the few, don't try.
source_stated_remedies: do not attempt humour unless you are one of the few who can write it
caveats: the reversal is dated rather than explained: the source says humour can NOW sell, implying a change in audiences rather than a [...] | the finding is attributed to a wave of factor analysis with no result, sample or date given — measurement asserted, result withheld | the execution caveat does most of the work: a technique that only a few practitioners can execute is not usable guidance for most [...]
GUARD relations (closure must cite, conflict-list or waive each partner): qualifies → sk_ogx_0031 (an example of the brand-preference measure overturning a received rule)

### sk_ogx_0039  (ogilvy-beyond-ch2)  label: brand_attribution_fails_by_default_and_must_be_forced_by_name_and_package
claim_type: explicit_source_claim  ·  scope: ['television_advertising']  ·  conditions: commercials of the period, particularly for new products
claim: The default outcome, according to the source, is that a viewer remembers the commercial and forgets which product it was for, often attributing it to a competing brand. Registering the brand is therefore treated as work that must be done deliberately rather than as a by-product of a good commercial. His stated devices are to use the name within the first ten seconds and to play games with it, such as spelling it out; he reports a commercial that repeated the brand name twenty times without irritating anyone. Commercials that end by showing the package are reported more effective at changing brand preference than those that do not. He notes many copywriters think it crass to belabour the name.
source_terms: Research has demonstrated that a shocking percentage of viewers remember your commercial, but forget the name of your product. All too often they [...] | Use the name within the first ten seconds. | Commercials which end by showing the package are more effective in changing brand preference than commercials which don't.
source_stated_problems: they attribute your commercial to a competing brand
source_stated_remedies: use the brand name within the first ten seconds | end by showing the package
caveats: the shocking percentage is never given, and the research demonstrating it is not identified — measurement asserted, result withheld | the twenty-repetitions example is anecdotal and its duration is stated oddly in the text, so the density it describes cannot be checked | misattribution to a competitor is a stronger failure than mere forgetting, because the advertising then works for the rival; the [...]

### sk_ogx_0040  (ogilvy-beyond-ch2)  label: the_first_frame_decides_whether_the_rest_is_seen_and_singularity_is_what_sticks
claim_type: explicit_source_claim  ·  scope: ['television_advertising']  ·  conditions: thirty-second commercials in the broadcast environment of the period
claim: With thirty seconds available, the source treats the first frame as the gate: grabbing attention there with a visual surprise gives a better chance of holding the viewer, and commercials are screened out because they open with something dull. He states the asymmetry that makes this a real failure — the maker knows great things are coming and the viewer does not, and will have left before finding out. His instruction is literal: when advertising fire extinguishers, open with the fire. Alongside this he says visual banality fails, since a viewer exposed to thirty thousand commercials a year lets most slide off memory, so a commercial needs a touch of singularity, a visual burr that sticks; and he reports that commercials with a plethora of short scenes are on average below average at changing brand preference, conceding that one colleague handles many scenes without confusing people and that he himself cannot.
source_terms: Open with the fire. You have only 30 seconds. If you grab attention in the first frame with a visual surprise, you stand a better chance of holding the viewer. | People screen out a lot of commercials because they open with something dull. You know that great things are about to happen, but the viewer doesn't. She [...] | you should give your commercials a touch of singularity, a visual burr that will stick in the viewer's mind
source_stated_problems: People screen out a lot of commercials because they open with something dull. | visual banality
source_stated_remedies: grab attention in the first frame with a visual surprise | show the viewer something she has never seen before
caveats: the thirty-second length, the thirty-thousand-commercials-a-year exposure and the six-hours-a-day set usage are all facts about [...] | no measurement is offered for the first-frame claim; the scene-change claim is stated as an average without the distribution | the viewer is referred to throughout as 'she', consistent with the period's assumption about who watches daytime television
GUARD relations (closure must cite, conflict-list or waive each partner): trades_off_with → sk_ogx_0039 (the first ten seconds must carry both the surprise and the brand name)

### sk_sb_c003_0014  (miller-storybrand-sb7)  label: three_questions_that_must_be_answerable_at_any_moment
claim_type: explicit_source_claim  ·  scope: ['storytelling', 'screenwriting', 'marketing']  ·  conditions: narrative content of any length
claim: A test the source applies to stories: at no point should it be possible to stop a film and be unable to say what the hero wants, what opposes them, and what their life will look like either way. It adds a deadline — if the three cannot be answered in the first fifteen to twenty minutes, the story has already failed.
source_terms: 1. What does the hero want? 2. Who or what is opposing the hero getting what she wants? 3. What will the hero's life look like if she does (or does not) [...] | if these three questions can't be answered within the first fifteen to twenty minutes, the story has already descended into noise
source_stated_problems: the story has descended into noise
caveats: the fifteen-to-twenty-minute threshold is stated without derivation and is the only quantity in the source's story argument | the box-office consequence attached to it is asserted, not evidenced

### sk_vig_c003_0013  (vignelli-canon-intangibles)  label: an_established_logo_holds_equity_that_should_be_protected
claim_type: explicit_source_claim  ·  scope: ['graphic_design', 'corporate_identity']  ·  conditions: established marks with long public exposure
claim: Requests to redesign a logo are often motivated by a desire for change merely for its own sake, which the source calls a very wrong motivation. A real corporate identity rests on an overall system rather than on a logo alone. A logo gradually becomes part of collective culture, and one in the public domain for more than fifty years becomes a classic and a landmark that should not be discarded for a new one however well designed. The source reports proposing a light retouch of the existing mark rather than a replacement when asked to design a new logo for Ford, and doing the same for Ciga Hotels, Cinzano and Lancia.
source_terms: A real Corporate Identity is based on an overall system approach, not just a logo. | When a logo has been in the public domain for more than fifty years it becomes a classic, a landmark, a respectable entity
source_stated_problems: the desire of change merely for the sake of change
source_stated_remedies: propose a light retouch of an established mark rather than a replacement | treat corporate identity as an overall system rather than as a logo
caveats: the source grounds the position partly autobiographically, in having grown up where history and vernacular architecture were treated [...] | the fifty-year threshold is stated without derivation; the cases named are all ones where the source's own recommendation was retention

### sk_whip_0011  (sullivan-hey-whipple)  label: an_idea_without_a_conflict_has_no_story_to_run_on
claim_type: explicit_source_claim  ·  scope: ['advertising_concept_development', 'brand_communication', 'television_advertising']  ·  conditions: brand storytelling and the writing of briefs; he allows conflicts as large as good versus evil or as small as a brand against a category annoyance
claim: Sullivan holds that a brand story requires an opposing force, and that most briefs remove it. The common brief describes life after purchase — a world with no cavities, no breakdowns, no overdrafts — which he says cuts to the end of the movie and short-circuits the structure that makes a story hold attention. His stated diagnosis of an uninspiring brief is that it states a solution rather than a problem, and he says creativity happens in response to a problem, so a brief phrased as a solution gives the maker nothing to respond to. He offers a headline test for the same point: nobody reads "Area Bank Not Robbed", not because the reader is bad but because attention tunes out an unchanged status quo.
source_terms: if you don't have conflict, you don't have a story | Area Bank Not Robbed | creativity happens in response to a problem
source_stated_problems: many clients want you to cut right to the end of the movie | solutions are about as interesting as filled-in crossword puzzles | the structure of life-is-better-with-our-product is still how many briefs are written
source_stated_remedies: identify and leverage the central conflicts within your client's company or category | if a conflict isn't immediately apparent, make one up
caveats: the jungle-alarm argument is quoted from a trade book and reasons from animal behaviour to advertising response; no advertising [...] | the source qualifies his own claim in the text — this is not an argument for negative advertising, and he says so | his named exemplars (FedEx, got milk?, Allstate 'Mayhem') are celebrated campaigns; campaigns that used conflict and failed are not [...]
GUARD relations (closure must cite, conflict-list or waive each partner): depends_on → sk_whip_0013 (deprivation is the specific conflict shape he most often reaches for)

### sk_whip_0031  (sullivan-hey-whipple)  label: exaggeration_is_the_default_technique_and_is_usually_reached_for_before_thinking
claim_type: explicit_source_claim  ·  scope: ['advertising_concept_development', 'television_advertising', 'print_advertising']  ·  conditions: concept generation; the source explicitly says it is not off-limits
claim: Sullivan places exaggeration deliberately last on his list of concepting techniques and explains why: it is used so commonly that it is the first technique juniors apply, and its first hundred outputs are predictable inversions of the product benefit. He does not forbid it — he says great ideas do use it — but requires the maker to notice when they are using it. He adds Pete Barry's condition: an exaggeration must be based on a truth, or what remains is a silly contrivance, and quotes Teressa Iezzi's name for the degenerate form, the advertisement in which someone is so distracted by the product that they fail to notice some outrageous event.
source_terms: the ol' exaggeration thing | a silly contrivance
source_stated_problems: it's just a little too easy | otherwise, you have only a silly contrivance | 'I'm so distracted by the awesome nature of this product that I didn't notice [outrageous visual phenomenon]'
source_stated_remedies: just be aware when you're using it | if you're going to do an exaggeration scenario, make sure you base it on a truth
caveats: the source states the objection is frequency of use and thoughtlessness of application rather than the device itself, and says so [...] | the 'based on a truth' requirement is quoted from another author and no test is given for when an exaggeration is sufficiently grounded

### sk_whip_0058  (sullivan-hey-whipple)  label: humour_is_subordinate_to_interest_and_is_not_always_the_right_register
claim_type: explicit_source_claim  ·  scope: ['copywriting', 'advertising_concept_development']  ·  conditions: choosing tone for a piece; the source is a practitioner of comic advertising and is arguing against his own default
claim: Sullivan subordinates humour explicitly. Funny is a subset of interesting; it is not a language but an accent; and it may not even be the right accent for a given client. His stated ordering is that funny, serious and heartfelt are all irrelevant unless the work is interesting first. Elsewhere he supplies the constraint that decides the register: the emotional choice is always a combination of what the product is and who is being addressed, and he gives the negative case — slapstick does not belong on a hospital's website.
source_terms: don't set out to be funny; set out to be interesting | funny is a subset of interesting | funny isn't a language, funny is an accent
source_stated_problems: none of it matters if you aren't interesting first
source_stated_remedies: study your product, brand, or category, and find the emotional center | pick a mood; a feeling; sometimes making this decision can give you focus
caveats: the claim is a definition offered as an argument; nothing establishes the subset relation beyond the author's assertion | the source's own examples throughout the book are overwhelmingly comic, which is a selection his stated position does not require
GUARD relations (closure must cite, conflict-list or waive each partner): qualifies → sk_whip_0005 (names what the clever half must actually deliver)
## OUTPUT
Write the JSON object to /tmp/blind/ac072eae.json (create the directory). Then reply with one line: the path and the number of beats.
