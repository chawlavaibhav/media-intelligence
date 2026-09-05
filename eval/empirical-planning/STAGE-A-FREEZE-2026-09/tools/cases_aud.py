# -*- coding: utf-8 -*-
from common import *

S1 = "इस दवाई से मेरी फसल दोगुनी हुई"
S2 = "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par."
S3 = "Zero petrol. Zero noise. All city."
DRIVE_CAP = 70  # characters; ≈ ≤ 5 s spoken, so the line ends inside the 6-s lipsync plate (Auditor AF-4)
assert all(len(s) <= DRIVE_CAP for s in (S1, S2, S3)), [len(s) for s in (S1, S2, S3)]
DRIVE_RULE = "drive = repeat 1 of ElevenLabs v3 for this script (frozen rule; the Controller may choose Sarvam in the morning — decision 9); the same drive file is held constant across both lipsync routes"
PLATE = "the Controller-accepted VID-I2V-02 clip (6 s, one man, static camera) — one plate held constant across all three lipsync cases so that the drive language is the only variable; for TOPO-01 the plate's subject (a young man in a lobby) differs from arm A's farmer in a field — the spoken line and the brief shape (one visible Hindi speaker, one line) are the same; the subject difference is recorded as the residual confound (Auditor AF-2)"

def aud_lang(code, n_speakers=1):
    return dict(LANG_TOPO[code], n_speakers=n_speakers, speaker_turn_boundaries_present=False)

def tts_routes(script, conditional_hindi=False):
    rs = [rt("sarvam-bulbul-v3", "native", "1b", dict(script=script, chars=len(script), voice="one male voice, chosen by ear at dispatch and recorded", language_code="as the script"), len(script), quantity_unit="chars"),
          rt("elevenlabs-v3", "native", "1b", dict(script=script, chars=len(script), voice="one male voice, recorded", model="eleven_v3"), len(script), quantity_unit="chars")]
    if conditional_hindi:
        rs += [rt("chirp-3-hd-hi-in", "conditional", "1b", dict(script=script, chars=len(script), voice="hi-IN male"), len(script), quantity_unit="chars"),
               rt("azure-neural-tts-hi-in", "conditional", "1b", dict(script=script, chars=len(script), voice="hi-IN male"), len(script), quantity_unit="chars")]
    return rs

def lip_routes(script):
    return [rt("sync-lipsync-v3", "chain", "1b", dict(plate=PLATE, drive=DRIVE_RULE, output_seconds=6, script=script), 6, quantity_unit="seconds"),
            rt("kling-lipsync-a2v", "chain", "1b", dict(plate=PLATE, drive="same drive file as sync-lipsync-v3", billed_input_seconds="10 (6-s plate rolled up to the 5-s increment)", script=script), 10, quantity_unit="seconds")]

AUD = []

def tts_case(cid, lang, text, attachments, source, script, voice_desc, pool_note, contract, irr, freshness=None, ambiguity=None, fixture_note=None):
    return dict(
        case_id=cid, lane="AUD",
        question_served=dict(plan_c1_rows=["best TTS route"] + (["best Hindi / Hinglish route (COND-LANGUAGE)"] if lang != "en" else []), roster_questions=["AUD-01", "AUD-02"], topo_arms=["TOPO-01 arm B (drive)"] if cid == "AUD-TTS-01" else [], c3d=[], freshness_items=freshness or []),
        customer_request=dict(channel="whatsapp", register="whatsapp", language=lang, text=text, attachments_named=attachments),
        source=source,
        nr=dict(requested_operation="generate", modality="audio", supplied_assets=[], mutation_intents=None,
            deliverable_set=dict(cardinality=1, variation_axis="none", acceptance_basis="per_deliverable"),
            product_or_packshot_present=False, entities=[], relationships=[],
            text_requirements=[], brand_requirements=None,
            language_topology=dict(spoken={"hi": "hi", "hg": "hi-en (Hinglish)", "en": "en-IN"}[lang], on_screen_copy="none", subtitles="none", viewer_locale="IN"),
            speaker_topology=dict(visible_speakers=0, offscreen_voices=1, turn_boundaries_required=False, script_exactness="exact", script=script),
            temporal_structure=None, subject_motion=None, camera_motion=None,
            delivery=dict(platform="audio file for a video edit", aspect_ratios=[], resolution="wav or mp3, as the route returns", safe_areas=[]),
            specification_provenance=dict(customer_specified=["R01", "R05", "R10", "R11", "R15", "R18"], customer_omitted=["R06", "R08", "R09", "R12"], derived=[]),
            ambiguity_markers=ambiguity or [],
            acceptance_intent=dict(stated_success_criteria=[voice_desc], stated_rejection_criteria=[], hard_constraints=["the script, word for word", "one voice"], soft_preferences=[], free_choices=["which voice, within the stated gender and register"]),
            provenance=prov(requested_operation="customer_stated", modality="customer_stated", language_topology="customer_stated", speaker_topology="customer_stated", delivery="customer_stated", acceptance_intent="customer_stated")),
        capabilities=dict(primary="spoken_script_correctness", exercised=["spoken_script_correctness", "pronunciation_intelligibility", "emotional_prosodic_fit", "delivery_format_compliance", "latency_errors_refusals", "reproducibility", "cost_and_cpao", "reliability_pass_at_k"]),
        conditions=conds(cid,
            delivery=dict(aspect_ratio="not_applicable", resolution="audio: route default sample rate (recorded)", duration_s="as spoken (≈ 2–6 s)", fps="not_applicable", delivery_size_declared=True, platform_target="audio_file"),
            load=dict(n_people=0, n_products=0, n_countable_objects=0, distractor_present=False, scene_complexity_class="not_applicable"),
            constraint=dict(n_hard_constraints=2, exact_string_count=1, exact_string_length_chars=len(script), brand_constraint_count=1 if "Kaushal" in script else 0, prerequisite_depth=0),
            workflow_modes={"Sarvam bulbul:v3, ElevenLabs v3 (+ conditional Chirp 3 HD / Azure Neural)": "tts"}, language=aud_lang(lang), operation="generate"),
        reference_assets=[],
        acceptance_contract=contract,
        routes=tts_routes(script, conditional_hindi=(cid == "AUD-TTS-01")),
        downstream_reuse=dict(feeds=[f"AUD-LIP-0{cid[-1]} drive (ElevenLabs repeat 1 by the frozen rule)"], consumes=[]),
        cut_order_rank=None, irreducibility_ref="C." + cid, irreducibility=irr,
        bp=dict(advertising=True, audio=True, decisions=[], text_handling="none (audio)",
                dispatch=dict(format="wav preferred, mp3 accepted", audio="the deliverable", reference_slots=0, max_chars=250),
                brief_parameters=[f"script (exact, {len(script)} characters): {script}", voice_desc, "one voice, no music bed, no effects", "pace: natural; a short pause at each sentence boundary"] + ([fixture_note] if fixture_note else []),
                prompt=script),
        pool_note=pool_note,
    )

AUD.append(tts_case("AUD-TTS-01", "hi",
    "एक voice-over line चाहिए हमारे किसान वाले video के लिए, video अलग से बन रहा है। पुरुष आवाज़, किसान जैसी सादी हिंदी, भरोसेमंद, ज़्यादा नाटकीय नहीं। Line है: \"इस दवाई से मेरी फसल दोगुनी हुई\"। बस यही, सिर्फ audio file (wav या mp3) भेज दीजिए।", [],
    dict(pool="brief_bank", id="BR-F07-HI", adaptation=["spoken_line_extracted_as_a_tts_request (the source is the 20-s farmer testimonial video; the same Nashik dealer asks for the line as a VO for a separate edit)", "line_shared_with_VID-T2V-01_after_audit (AF-2: TOPO-01 arm A and arm B now carry the same brief and the same spoken line; the first draft used BR-F05-HI's detergent line, which is no longer in the package)", "voice_gender_stated_male (the source's speaker is a farmer, male by the source's own pronoun; chosen so the same voice can drive the male-plate lipsync cases)", "register_rewritten_to_devanagari_whatsapp", "source flag carried: the line is an efficacy claim presented as testimony"]),
    S1, "male voice, plain farmer-like Hindi, trustworthy, not theatrical", "Sarvam credits + ElevenLabs cash; Chirp 3 HD / Azure Neural TTS conditional credit-only extras on this Hindi script",
    ["ACCEPT only if a first-language Hindi listener hears exactly \"इस दवाई से मेरी फसल दोगुनी हुई\" — every word, in order, no extra word.",
     "ACCEPT only if it is one male voice speaking clear Hindi; REJECT if any word is heard as a different word (e.g. दवाई or दोगुनी mispronounced into another word).",
     "REJECT if any music, effect, second voice or English word is present.",
     "REJECT if the file is silent, truncated mid-word, or longer than 6 seconds."],
    "Drop it and AUD-01/02 have no Hindi script and TOPO-01 arm B has no drive for the arm-A line; it cannot merge with AUD-TTS-02 because Hindi and Hinglish results are never pooled and code-mixing is the harder, more commercial case.", freshness=[5]))

AUD.append(tts_case("AUD-TTS-02", "hg",
    "Ek VO chahiye 15 sec ke video ke liye, young male voice, energetic aur motivational, but bharosa bhi lage, padhai ka matter hai. Thoda fast bole but clear. Line: \"Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par.\" Hindi-English mix hai, waise hi bolna hai jaise hum bolte hain. Kaushal Setu hamara naam hai, sahi bolna. Sirf audio chahiye.", [],
    dict(pool="brief_bank", id="BR-F07-HG", adaptation=["spoken_script_extracted_as_a_tts_request (the source is a 15-s single-speaker video; here the VO alone)", "brand_name_line_added_as_fixture ('Kaushal Setu par' appended: the task requires Indian brand names in the Hinglish script and the source's business is unnamed; the name is a labelled fixture, not customer text from the bank)", "script_shortened_to_drive_cap (AF-4: 'Toh' dropped and the clauses tightened so the line is ≤ 70 characters, ≈ ≤ 5 s, and ends inside the 6-s lipsync plate)", "register_rewrite_after_audit (the source's mid-sentence Devanagari 'enroll करो' typed in Latin as a Hinglish buyer types; 'education hai' → 'padhai ka matter hai')", "end_card_dropped (\"Batch starts Monday\")", "both source contradictions kept (energetic vs calm; fast vs clear)"]),
    S2, "young male voice, energetic and motivational yet trustworthy; a little fast but every word clear", "Sarvam credits + ElevenLabs cash",
    ["ACCEPT only if the listener hears exactly \"Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par.\" — every word, in order.",
     "ACCEPT only if \"Kaushal Setu\" is heard as the Hindi words कौशल सेतु; REJECT if either word is heard as something else.",
     "ACCEPT only if every word, English and Hindi, is understood on a single listen by a Hindi-English speaker; REJECT if any word has to be replayed to be made out.",
     "REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds."],
    "Drop it and the TTS lane has no code-mixed script, which the condition contract calls arguably the hardest and most commercially common case, and the brand-name pronunciation question (human-judged, Q5) has no item; it cannot merge with AUD-TTS-01 (pure Hindi) or AUD-TTS-03 (English) for the pooling rule.",
    ambiguity=[dict(marker_type="contradiction", detail="energetic vs calm/trustworthy; fast vs clearly understood (source c1, c2) — recorded; the request's own words are the resolution ('thoda fast but clearly')", affected_fields=["R18"])],
    fixture_note="fixture note: the brand name Kaushal Setu is a labelled fixture; no real business of that name is implied"))

AUD.append(tts_case("AUD-TTS-03", "en",
    "Need the VO for our scooter film. Calm male voice, Indian English accent, not American or British. Script exactly: \"Zero petrol. Zero noise. All city.\" Three short sentences with a small pause between each. Just the audio file please, wav if possible.", [],
    dict(pool="brief_bank", id="BR-F05-EN", adaptation=["voiceover_script_extracted_as_a_tts_request (the source is a 15-s scooter film with this VO)", "accent_stated_indian_english (the source says 'calm male voice'; the Indian-English condition is the lane's stated shape)", "end_text_dropped (\"Book now at velo.in\")"]),
    S3, "calm male voice, Indian English accent", "Sarvam credits + ElevenLabs cash",
    ["ACCEPT only if the listener hears exactly \"Zero petrol. Zero noise. All city.\" — three sentences, no added or missing word.",
     "ACCEPT only if there is an audible pause between each sentence.",
     "ACCEPT only if the accent is recognisably Indian English; REJECT if it is American or British.",
     "REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds."],
    "Drop it and the TTS lane has no English control against which the Hindi and Hinglish results are read (they are never pooled, but the English row is what shows a route's Indic weakness is language-specific); it cannot merge with the others for the pooling rule."))

# ---------------------------------------------------------------- lipsync cases
def lip_case(cid, lang, text, attachments, drive_case, script, contract, irr, freshness=(5,)):
    return dict(
        case_id=cid, lane="AUD",
        question_served=dict(plan_c1_rows=["best lip-sync route"] + (["best Hindi / Hinglish route (COND-LANGUAGE)"] if lang != "en" else []), roster_questions=["AUD-03"], topo_arms=["TOPO-01 arm B"] if cid == "AUD-LIP-01" else [], c3d=[], freshness_items=list(freshness)),
        customer_request=dict(channel="whatsapp", register="whatsapp", language=lang, text=text, attachments_named=attachments),
        source=dict(pool="fixture", id="none", adaptation=[f"fixture — no source pool holds a 'lip-sync this voice onto this clip' request; the shape is the Media Factory LatentSync route (freshness item 5) and TOPO-01 arm B; the drive is the {drive_case} output and the plate is the VID-I2V-02 accepted clip, so the case consumes two real-demand items", "register_rewrite_after_audit (the timing / closed-lips clauses that restated the contract were removed; the buyer asks for a natural lip-sync and the contract carries the timing and silence tests)"], derived_from=[drive_case, "VID-I2V-02"]),
        nr=dict(requested_operation="compose", modality="video",
            supplied_assets=[dict(asset_id=attachments[0].split(".")[0], media_type="video", role="subject_of_operation", applies_to="presenter", description="6-s clip of one man, static camera (the VID-I2V-02 accepted clip)"),
                             dict(asset_id=attachments[1].split(".")[0], media_type="audio", role="subject_of_operation", applies_to="voice", description=f"the VO file: \"{script}\"")],
            mutation_intents=dict(preservation_default="implicit_everything_not_named", intents=[dict(target="mouth movement", intent="change", detail="must match the supplied voice in time and shape"), dict(target="everything else in the clip", intent="preserve", detail="customer named this: face, background, rest of the clip unchanged"), dict(target="lips when no speech", intent="preserve", detail="closed / at rest during silence — customer named this")]),
            deliverable_set=dict(cardinality=1, variation_axis="none", acceptance_basis="per_deliverable"),
            product_or_packshot_present=False,
            entities=[dict(entity_id="presenter", entity_type="person", role="hero", identity_invariants=["face as in the clip"])],
            relationships=[dict(subject="presenter", relation="speaks", object="voice")],
            text_requirements=[], brand_requirements=None,
            language_topology=dict(spoken={"hi": "hi", "hg": "hi-en (Hinglish)", "en": "en-IN"}[lang], on_screen_copy="none", subtitles="none", viewer_locale="IN"),
            speaker_topology=dict(visible_speakers=1, offscreen_voices=0, turn_boundaries_required=False, script_exactness="exact", script=script),
            temporal_structure=dict(duration_seconds=6, shot_count=1, beats=[dict(beat=1, content="the line is spoken; silence after")], continuity_requirements=["identity unchanged"]),
            subject_motion=dict(entity_ref="presenter", motion_type="gesture", description="mouth moves with the voice"),
            camera_motion=dict(motion_type="static", description="as the supplied clip"),
            delivery=dict(platform="social", aspect_ratios=["as the clip (4:5)"], resolution="as the clip", safe_areas=[]),
            specification_provenance=dict(customer_specified=["R01", "R02", "R03", "R05", "R06", "R07", "R10", "R11", "R13", "R18"], customer_omitted=["R08", "R09", "R15"], derived=[dict(field="R12, R14, R15", rationale="as the supplied clip — follow from the preservation request")]),
            ambiguity_markers=[],
            acceptance_intent=dict(stated_success_criteria=["lips match the words and timing", "lips closed in silence"], stated_rejection_criteria=["anything else changed"], hard_constraints=["mouth matches the voice", "face and background unchanged", "lips at rest when no speech"], soft_preferences=[], free_choices=[]),
            provenance=prov(requested_operation="customer_stated", supplied_assets="customer_stated", mutation_intents="customer_stated", modality="customer_stated", entities="customer_stated", relationships="customer_stated", language_topology="customer_stated", speaker_topology="customer_stated", subject_motion="customer_stated", camera_motion="customer_implied", temporal_structure="customer_implied", delivery="customer_implied", acceptance_intent="customer_stated")),
        capabilities=dict(primary="single_speaker_lip_sync", exercised=["single_speaker_lip_sync", "audio_video_synchronisation", "person_stability_in_clip", "technical_visual_integrity", "delivery_format_compliance", "latency_errors_refusals", "reproducibility", "cost_and_cpao", "reliability_pass_at_k"]),
        conditions=conds(cid,
            delivery=dict(aspect_ratio="4:5 (as the clip)", resolution="as the clip (720p-class)", duration_s=6, fps="as the clip", delivery_size_declared=True, platform_target="social"),
            load=dict(n_people=1, n_products=0, n_countable_objects=1, distractor_present=False, scene_complexity_class="moderate"),
            motion=dict(camera_motion_class="static", subject_motion_class="mouth_only", motion_magnitude_class="low", framing_instruction="as the clip"),
            constraint=dict(n_hard_constraints=3, exact_string_count=1, exact_string_length_chars=len(script), brand_constraint_count=0, prerequisite_depth=2),
            workflow_modes={"sync-lipsync v3, Kling lipsync audio-to-video": "transform_lipsync"}, language=aud_lang(lang),
            inp=dict(input_source_class="controller_accepted_generated_clip + generated_tts", input_resolution="720p-class", input_degradation_class="none"),
            operation="compose", ref_prov="benchmark_fixed (plate and drive are accepted 1b outputs)"),
        reference_assets=[dict(role="supplied_subject", description=PLATE, rights_rule="generated in this programme", decoys_required=False, status="specified (bytes exist after 1b i2v acceptance)"),
                          dict(role="supplied_subject", description=f"drive audio: {DRIVE_RULE}", rights_rule="generated in this programme", decoys_required=False, status="specified (bytes exist after the TTS calls)")],
        acceptance_contract=contract,
        routes=lip_routes(script),
        downstream_reuse=dict(feeds=[], consumes=["VID-I2V-02 accepted clip (plate)", f"{drive_case} ElevenLabs repeat 1 (drive)"]),
        cut_order_rank=None, irreducibility_ref="C." + cid, irreducibility=irr,
        bp=dict(advertising=True, audio_half=True,
                decisions=[("CA-D11", "No camera move is added; the supplied clip's stillness is kept (ms_0002)."),
                           ("CA-D1", "The 1st read must remain the face; the transform may not introduce a new cue (a mouth region that flickers or shifts tone competes with the eyes, ms_0019)."),
                           ("CA-D3", "Framing unchanged; no re-crop of the plate.")],
                text_handling="none",
                dispatch=dict(aspect="as the clip", duration_s=6, resolution="as the clip", audio="the supplied drive, muxed unchanged", reference_slots="2 (clip + audio)"),
                brief_parameters=["plate: " + PLATE, "drive: " + DRIVE_RULE, f"drive script ≤ {DRIVE_CAP} characters (≈ ≤ 5 s spoken) so the line ends inside the 6-s plate and the after-line silence is judgeable (AF-4); this script: {len(script)} characters", "no speaker mask supplied (one face)", "output audio = the drive, unchanged; video = the plate with the mouth region re-synthesised only"],
                prompt=f"Lip-sync the supplied voice onto the supplied clip. The man's mouth must move with the words \"{script}\" in time and shape; when the voice is silent his lips rest closed. Change nothing else: face, hair, background, framing and timing of the clip stay exactly as supplied."),
    )

AUD.append(lip_case("AUD-LIP-01", "hi",
    "हमारे presenter की एक clip है (presenter_clip.mp4, 6 सेकंड) और किसान वाली line की VO है (vo_kisan.wav) — \"इस दवाई से मेरी फसल दोगुनी हुई\"। इस आवाज़ को clip पर lip-sync कर दीजिए, natural लगे। चेहरा, background, बाकी सब वैसा ही रहे।",
    ["presenter_clip.mp4", "vo_kisan.wav"], "AUD-TTS-01", S1,
    ["ACCEPT only if the man's mouth opens and closes with the syllables of \"इस दवाई से मेरी फसल दोगुनी हुई\" — a first-language Hindi judge sees the words being spoken; REJECT if the mouth moves out of time by a visible beat.",
     "ACCEPT only if his lips are closed or at rest during the silence after the line.",
     "REJECT if the face changes identity, the mouth region shows a visible patch, blur, colour seam or flicker, or the background changes.",
     "REJECT if the audio in the output is not the supplied voice (re-synthesised, clipped or shifted)."],
    "Drop it and TOPO-01 has no arm B and freshness item 5 (LatentSync-class mouth repaint vs native lip-sync) is untested for Hindi; it cannot merge with VID-T2V-01 (arm A) because the two arms are the comparison, nor with AUD-LIP-02/03 for the language-pooling rule."))

AUD.append(lip_case("AUD-LIP-02", "hg",
    "Ek clip hai instructor ki (instructor_clip.mp4, 6 sec) aur VO file (vo_kaushal.wav) — \"Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par.\" VO ko clip pe lip-sync kar do, natural lage. Baaki clip mein kuch change nahi, face same.",
    ["instructor_clip.mp4", "vo_kaushal.wav"], "AUD-TTS-02", S2,
    ["ACCEPT only if the mouth follows the whole line \"Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par.\" in time — including the English words — with no visible lag or lead.",
     "ACCEPT only if the lips rest closed during the pauses and after the line.",
     "REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.",
     "REJECT if the output audio is not the supplied voice."],
    "Drop it and the lip-sync lane has no code-mixed drive, so a route that syncs Hindi syllables but not English ones inside a Hindi sentence would pass unseen; it cannot merge with the other two for the pooling rule."))

AUD.append(lip_case("AUD-LIP-03", "en",
    "Sending a 6 sec clip of our presenter (presenter_clip.mp4) and the VO (velo_vo.wav) - \"Zero petrol. Zero noise. All city.\" Please lip-sync the VO onto the clip so it looks natural. Nothing else in the clip should change.",
    ["presenter_clip.mp4", "velo_vo.wav"], "AUD-TTS-03", S3,
    ["ACCEPT only if the mouth follows \"Zero petrol. Zero noise. All city.\" in time, sentence by sentence.",
     "ACCEPT only if the lips are closed in each of the two pauses and after the last sentence.",
     "REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.",
     "REJECT if the output audio is not the supplied voice."],
    "Drop it and the lip-sync lane has no English row to show whether a route's Hindi failure is language-specific or general; it cannot merge with the other two for the pooling rule."))

# ---------------------------------------------------------------- music cases
def mus_case(cid, lang, text, source, brief_params, contract, irr, prompt):
    return dict(
        case_id=cid, lane="MUS",
        question_served=dict(plan_c1_rows=["(§C.3d music lane — no §C.1 row; recorded as added scope)"], roster_questions=["none (added scope; no August slot)"], topo_arms=[], c3d=["music lane"], freshness_items=[]),
        customer_request=dict(channel="whatsapp", register="whatsapp", language=lang, text=text, attachments_named=[]),
        source=source,
        nr=dict(requested_operation="generate", modality="audio", supplied_assets=[], mutation_intents=None,
            deliverable_set=dict(cardinality=1, variation_axis="none", acceptance_basis="per_deliverable"),
            product_or_packshot_present=False, entities=[], relationships=[], text_requirements=[], brand_requirements=None,
            language_topology=dict(spoken="none", on_screen_copy="none", subtitles="none", viewer_locale="IN"),
            speaker_topology=dict(visible_speakers=0, offscreen_voices=0, turn_boundaries_required=False, script_exactness="free"),
            temporal_structure=dict(duration_seconds=30, shot_count=None, beats=[], continuity_requirements=["loopable if possible"]),
            subject_motion=None, camera_motion=None,
            delivery=dict(platform="music bed for a video edit", aspect_ratios=[], resolution="wav preferred", safe_areas=[]),
            specification_provenance=dict(customer_specified=["R01", "R05", "R10", "R11 (none)", "R12.duration", "R15", "R18"], customer_omitted=["R06", "R08", "R09"], derived=[]),
            ambiguity_markers=[],
            acceptance_intent=dict(stated_success_criteria=brief_params[:2], stated_rejection_criteria=["vocals", "big cinematic swell / filmy"], hard_constraints=["30 s", "no vocals"], soft_preferences=brief_params[2:], free_choices=["key, tempo"]),
            provenance=prov(requested_operation="customer_stated", modality="customer_stated", language_topology="customer_stated", temporal_structure="customer_stated", delivery="customer_stated", acceptance_intent="customer_stated")),
        capabilities=dict(primary="emotional_prosodic_fit", exercised=["emotional_prosodic_fit", "delivery_format_compliance", "latency_errors_refusals", "reproducibility", "cost_and_cpao", "reliability_pass_at_k"], note="no music-specific capability exists in contract v2; emotional_prosodic_fit (register fit of an audio delivery) is the nearest active id; human-judged only"),
        conditions=conds(cid,
            delivery=dict(aspect_ratio="not_applicable", resolution="audio: route default (recorded)", duration_s=30, fps="not_applicable", delivery_size_declared=True, platform_target="music_bed"),
            load=dict(n_people=0, n_products=0, n_countable_objects=0, distractor_present=False, scene_complexity_class="not_applicable"),
            constraint=dict(n_hard_constraints=2, exact_string_count=0, exact_string_length_chars=0, brand_constraint_count=0, prerequisite_depth=0),
            workflow_modes={"Lyria (Vertex), ElevenLabs music (fal)": "generate (music)"}, language=aud_lang(lang, 0), operation="generate"),
        reference_assets=[],
        acceptance_contract=contract,
        routes=[rt("lyria", "native", "1b", dict(duration_s=30, format="wav"), 1, quantity_unit="clips"),
                rt("elevenlabs-music", "native", "1b", dict(duration_s=30, format="wav", billed_minutes="1 (30-s clip rounded up)"), 1, quantity_unit="minutes")],
        downstream_reuse=dict(feeds=[], consumes=[]),
        cut_order_rank=8 if cid == "MUS-02" else None, irreducibility_ref="C." + cid, irreducibility=irr,
        bp=dict(advertising=True, audio=True, decisions=[], text_handling="none (audio)",
                dispatch=dict(format="wav preferred", duration_s=30, audio="the deliverable", reference_slots=0),
                brief_parameters=brief_params, prompt=prompt),
    )

AUD.append(mus_case("MUS-01", "hi",
    "हमारे 15 सेकंड के kitchen वाले video के लिए background music चाहिए, 30 सेकंड का clip बना दीजिए, हम काट लेंगे। घर की रसोई वाला feel — हल्का, warm, थोड़ा Indian touch (बांसुरी या तबला हल्का सा), ज़्यादा filmy नहीं। कोई गाना या बोल नहीं, सिर्फ music। Loop हो सके तो अच्छा। wav भेज दीजिए।",
    dict(pool="brief_bank", id="BR-F06-HI", adaptation=["music_bed_extracted_from_the_video_brief (source: 'sirf background music aur kitchen ki awaaz' for a 15-s cooker demo; here the buyer asks for the bed alone)", "duration_set_to_30s (a bed to cut from)", "instrument_hint_stated (flute or light tabla) — the customer's own words for 'Indian touch'", "register_rewritten_to_devanagari_whatsapp"]),
    ["warm, light, home-kitchen feel", "a light Indian touch: flute or soft tabla", "not filmy", "loopable"],
    ["ACCEPT only if the track is 28–32 s long and has no sung or spoken words.",
     "REJECT if drums or heavy percussion dominate the mix, or if an orchestral string or brass swell is present.",
     "ACCEPT only if at least one recognisably Indian instrument colour (flute/bansuri or tabla-like percussion) is audible.",
     "REJECT if the file is silent, clipped or ends with an abrupt cut mid-phrase."],
    "Drop it and the §C.3d music lane has no Hindi-market bed and only one brief, which cannot show whether a route's register control is real; it cannot merge with MUS-02 (minimal Western beat) because the Indian-instrument colour is the condition.",
    "Instrumental background music, 30 seconds, no vocals, for a home-kitchen scene: light, warm and unhurried, gentle acoustic texture with a soft bansuri (Indian flute) line and a very light tabla pulse, everyday and homely rather than cinematic; steady enough to loop; no big swells."))

AUD.append(mus_case("MUS-02", "en",
    "Need a music track for our runner film - 30 seconds, we will cut it down. Early morning, empty street, building momentum, real not glossy - think a minimal beat that picks up, no vocals, no big cinematic swell. It should sit under ambient street sound, so not too busy. wav please.",
    dict(pool="brief_bank", id="BR-F06-EN", adaptation=["music_bed_extracted_from_the_video_brief (source: 'just music and ambient sound' for a 15-s runner film)", "duration_set_to_30s", "register_kept_email_style_whatsapp"]),
    ["minimal beat that builds momentum", "real, not glossy; sits under ambient street sound", "no big cinematic swell", "not too busy"],
    ["ACCEPT only if the track is 28–32 s long and has no sung or spoken words.",
     "ACCEPT only if the energy audibly builds from the start to the end (more elements or a stronger pulse by the last third).",
     "REJECT if there is a large orchestral or 'trailer' swell, or if the arrangement is so dense it would mask street ambience.",
     "REJECT if the file is silent, clipped or ends abruptly mid-phrase."],
    "Drop it and the music lane has one brief and cannot separate 'the route makes acceptable music' from 'the route makes this one mood'; it is eighth in the cut order because the Hindi bed carries the market condition.",
    "Instrumental music, 30 seconds, no vocals, for an early-morning city running film: a minimal, dry electronic-acoustic beat that starts sparse and builds momentum steadily, adding a pulse and a simple melodic figure by the last third; understated and real, never glossy or cinematic; leaves space for street ambience underneath."))
