#!/usr/bin/env python3
"""RES-001 :: rebuild source-registry-v0.csv and resources/sources/*.md from one place.
Acquisition counts/bytes are read from disk at run time, never hand-typed."""
import csv, json, os, subprocess

TS = "2026-08-24"
RAW = "resources/corpus/raw"
MEDIA_EXT = {".mp4",".mkv",".webm",".mov",".png",".jpg",".jpeg",".webp"}

def actual(sid):
    root = os.path.join(RAW, sid)
    n = b = 0
    for dp,_,names in os.walk(root):
        for f in names:
            if os.path.splitext(f)[1].lower() in MEDIA_EXT:
                n += 1; b += os.path.getsize(os.path.join(dp,f))
    return n, b

S = [
 dict(source_id="src_konvid1k", canonical_name="KoNViD-1k", domain="real_natural_video (Flickr/YFCC100M)",
  origin="MMSP / VQA Group, Universitat Konstanz", official_url="https://database.mmsp-kn.de/konvid-1k-database.html",
  citation="Hosu et al., QoMEX 2017", media_type="video",
  provided_labels="subjective quality MOS + per-video blur/colourfulness/contrast/SI/TI/VNIQE (KoNViD_1k_attributes.csv, KoNViD_1k_mos.csv)",
  human_annotation_type="crowdsourced subjective quality study", dataset_size_claimed="1,200 videos, 8s each, ~2.3 GB",
  access_method="public direct download, ungated: https://datasets.vqa.mmsp-kn.de/archives/KoNViD_1k_videos.zip . No login/form/cookie. robots.txt absent on the file host; the database host does not disallow the KoNViD-1k page.",
  code_license="n/a", dataset_annotation_license="not_stated",
  underlying_media_rights="not_verified. Official page describes sources as Creative Commons video from YFCC100M but names no variant. The distributed metadata contains flickr_id but NO per-video licence field — checked directly. Per-item CC status therefore unresolved.",
  redistribution_status="not_stated - treat as NOT permitted",
  commercial_use_status_if_explicit="not_stated",
  terms_access_notes="Acquired under RES-001 clarification 6/7: public, ungated, no explicit term prohibiting download, internal research/evaluation only. flickr_id is present, so a future rights review could resolve per-video CC status against Flickr if a use beyond internal evaluation is ever proposed. PRIVACY: the distributor's KoNViD_1k_subjective.csv shipped crowdworker IP addresses, worker IDs and city/region/country. DELETED 24 Aug 2026 under explicit Controller approval (RES-002 finalization item 5); no redacted copy kept. Aggregate MOS (KoNViD_1k_mos.csv) and per-video technical attributes are retained and contain no personal data. See resources/reports/RES-002-privacy-deletion-log.md.",
  version="full public release", status="downloaded",
  reason="Public, ungated, no explicit prohibition. Rights not_stated and recorded as such. Provides the only large real human-made media in the pilot."),

 dict(source_id="src_youtube_ugc", canonical_name="YouTube-UGC", domain="real_ugc_video (YouTube creators)",
  origin="Google / YouTube Media Algorithms", official_url="https://media.withyoutube.com/",
  citation="Wang, Inguva, Adsumilli, MMSP 2019 (arXiv:1904.06457)", media_type="video",
  provided_labels="no-reference quality metrics published separately (Noise, Banding, SLEEQ); subjective MOS in follow-up work",
  human_annotation_type="subjective quality study (separate release)", dataset_size_claimed="~1,500 clips; bucket holds 1,070 video keys / 4,922 objects",
  access_method="public Google Cloud Storage bucket `ugc-dataset`, anonymous HTTP, ungated. Anonymous XML listing returns HTTP 200. NOT retrieved from youtube.com - no YouTube endpoint touched, so YouTube's robots.txt/ToS restrictions on /get_video are not engaged.",
  code_license="n/a", dataset_annotation_license="see media licence",
  underlying_media_rights="EXPLICIT AND VERIFIED. gs://ugc-dataset/LICENSE is a Creative Commons Public License. gs://ugc-dataset/ATTRIBUTION names each clip's original work, author and states 'licensed under CC BY 4.0'. Clips are audio-removed excerpts of CC BY 4.0 YouTube videos.",
  redistribution_status="CC BY 4.0 permits redistribution with attribution; we do not redistribute",
  commercial_use_status_if_explicit="CC BY 4.0 does not restrict commercial use (licence text read directly)",
  terms_access_notes="Best-documented source in the pilot: explicit licence AND per-item attribution. LICENSE and ATTRIBUTION retained alongside the media. Selection is deterministic and content-blind: within the 360P tier, the first clip of each distributor-defined category in sorted order, until the source byte budget. Rate-limited, sequential, 1s delay.",
  version="360P tier, one clip per category, bounded sample", status="partial_download",
  reason="Explicitly CC BY 4.0, ungated, official Google distribution. Bounded sample only because original pre-transcode files are 0.06-5 GB each."),

 dict(source_id="src_imagerewarddb", canonical_name="ImageRewardDB", domain="generated_image_preference",
  origin="Zhipu/THUDM (ImageReward, NeurIPS 2023)", official_url="https://huggingface.co/datasets/zai-org/ImageRewardDB",
  citation="Xu et al., ImageReward, NeurIPS 2023", media_type="image",
  provided_labels="expert pairwise comparisons; separate alignment / fidelity / harmlessness ratings",
  human_annotation_type="expert human annotation", dataset_size_claimed="137k expert comparisons; images/ tree = 23.7 GB (train 21.4, test 1.18, validation 1.13)",
  access_method="public HuggingFace, anonymous, ungated. NOTE: THUDM/ImageRewardDB now HTTP 307-redirects to zai-org/ImageRewardDB (org rename) - the URL printed in CORPUS-SOURCING-PLAN.md era references is stale.",
  code_license="MIT (stated)", dataset_annotation_license="apache-2.0 (stated on dataset card)",
  underlying_media_rights="not_verified beyond the publisher's assertion. Images collected from DiffusionDB (Stable Diffusion generations). Publisher asserts apache-2.0 over the dataset.",
  redistribution_status="apache-2.0 permits redistribution; we do not redistribute",
  commercial_use_status_if_explicit="not_stated explicitly; apache-2.0 imposes no use restriction",
  terms_access_notes="Subset rule is the distributor's own COMPLETE validation split, taken whole - so no selection judgement of ours enters the corpus at all. Full dataset far exceeds the RES-001 budget.",
  version="official validation split (validation_1.zip + validation_2.zip)", status="partial_download",
  reason="Apache-2.0, ungated. Only source separating evaluation dimensions, closest public analogue to our technical-vs-creative split."),

 dict(source_id="src_videofeedback", canonical_name="VideoFeedback (VideoScore)", domain="generated_video_human_scores",
  origin="TIGER-Lab", official_url="https://huggingface.co/datasets/TIGER-Lab/VideoFeedback",
  citation="VideoScore / VideoFeedback, TIGER-Lab", media_type="video",
  provided_labels="visual quality, temporal consistency, dynamic degree, text-to-video alignment, factual consistency (1-4)",
  human_annotation_type="human raters, multi-aspect", dataset_size_claimed="card claims 37.6k pairs / 8.81 GB; the media repo's main revision exposes 987 mp4 files totalling 0.18 GB - the discrepancy is unexplained and recorded as observed",
  access_method="public HuggingFace, anonymous, ungated. Annotations at TIGER-Lab/VideoFeedback; media at hexuan21/VideoFeedback-videos-mp4.",
  code_license="not_stated", dataset_annotation_license="apache-2.0 (stated on both repos)",
  underlying_media_rights="not_verified beyond the publisher's assertion. AI-generated video from multiple text-to-video models plus some real-world video as augmentation; the card names neither the source models nor which items are the real-world portion.",
  redistribution_status="apache-2.0 permits redistribution; we do not redistribute",
  commercial_use_status_if_explicit="not_stated explicitly; apache-2.0 imposes no use restriction",
  terms_access_notes="No subset rule needed: every mp4 addressable on the media repo's main revision was taken. Temporal-consistency labels are the relevant axis for the cross-frame observation-unit problem.",
  version="all mp4 on main revision", status="downloaded",
  reason="Apache-2.0, ungated, fits budget whole."),

 dict(source_id="src_videogen_rewardbench", canonical_name="VideoGen-RewardBench", domain="generated_video_pairwise_preference",
  origin="KwaiVGI / Kling team", official_url="https://huggingface.co/datasets/KlingTeam/VideoGen-RewardBench",
  citation="VideoAlign, NeurIPS 2025", media_type="video",
  provided_labels="pairwise preference: visual quality, motion quality, temporal alignment, overall",
  human_annotation_type="expert annotators, pairwise", dataset_size_claimed="25,234 rows; videos.zip = 13.42 GB",
  access_method="public HuggingFace, anonymous, ungated. KwaiVGI/... 307-redirects to KlingTeam/... .",
  code_license="not_stated", dataset_annotation_license="apache-2.0 (stated)",
  underlying_media_rights="not_verified beyond the publisher's assertion. Video generated by 12 named models (CogVideoX, kling, kling1.5, qingying, gen3, minimax, vidu, tongyi, luma, luma1.6, opensora1.2, easyanimatev4). Whether a third party can licence outputs of commercial generators is not established.",
  redistribution_status="apache-2.0 permits redistribution; we do not redistribute",
  commercial_use_status_if_explicit="not_stated explicitly; apache-2.0 imposes no use restriction",
  terms_access_notes="STATUS CHANGED IN RES-002 from too_large_for_pilot to partial_download. RES-001 concluded a bounded subset was impossible because the media ship as one 13.42 GB videos.zip. That conclusion was WRONG: a zip stores its index at the end of the file, the host answers HTTP 206 (range requests), and so the member list can be read and individual members fetched by byte offset. The full archive was never downloaded or staged on disk. Reading the entire index cost 0.5 MB in 4 range requests (0.004% of the archive); acquiring 288 selected members brought total transfer to 0.78 GB (5.8%). Selection is 24 files per distributor-defined generator folder across all 12 generators, sorted order within each - equal representation rather than first-N, which would have over-represented whichever generator sorts first. Human preference labels retained in videogen-rewardbench.csv. No full-archive SHA256 is recorded because the archive was never downloaded; fabricating one would be dishonest. Reproduction metadata in _transient_acquisition.json.",
  version="288 members, 24 per generator x 12 generators (transient member-level acquisition)", status="partial_download",
  reason="Apache-2.0, ungated, host honours HTTP range. Member-level acquisition made the 12-generator diversity available at 5.8% of the archive transfer and zero long-term archive storage."),

 dict(source_id="src_bstd_devanagari", canonical_name="Bharat Scene Text Dataset - Devanagari subset", domain="real_scene_text_devanagari",
  origin="Bhashini / IIT Jodhpur", official_url="https://github.com/Bhashini-IITJ/BharatSceneTextDataset",
  citation="arXiv:2511.23071", media_type="image",
  provided_labels="per-image ground-truth transcription (Unicode) + language label, in train/test_recognition_data.json",
  human_annotation_type="manual annotation - polygon boxes, transcription, script", dataset_size_claimed="6,582 scene images / 126,292 words across 12 languages; recognition.zip = 829,120,510 bytes",
  access_method="public creator-published Google Drive link, no login. Anonymous requests get Google's standard large-file 'Virus scan warning' interstitial, which asks for no credential/account/agreement - JUDGEMENT CALL flagged in the Controller Brief.",
  code_license="not_stated", dataset_annotation_license="not_stated for annotations",
  underlying_media_rights="repo states images are under Creative Commons cc-by-sa-4.0. Annotation/transcription licence not stated -> not_verified.",
  redistribution_status="cc-by-sa-4.0 permits redistribution with share-alike for the images; annotation terms unstated; we do not redistribute",
  commercial_use_status_if_explicit="cc-by-sa-4.0 does not restrict commercial use for the images; annotations not_stated",
  terms_access_notes="TRANSIENT acquisition: the 0.83 GB archive was downloaded to temporary staging, only Devanagari members extracted, archive deleted after validation (sha256 159fb044fba701f87e41a98b679a5da8c4dadd07727a2a5de72bb9d4f2c13036 recorded first). Selection rule = UNION of (a) language label == hindi and (b) transcription contains a Devanagari codepoint. Rule (b) matters: Marathi is written in Devanagari and a language filter alone would have missed ~5,100 target-script images. 351 further images labelled as other languages also carry Devanagari text - the language label is NOT a reliable proxy for script.",
  version="Devanagari subset, 25,246 of 106,490 archive members", status="partial_download",
  reason="Largest Devanagari pool acquired: real photographed signage with human transcriptions, which is what checker calibration needs."),

 dict(source_id="src_indicstr12_devanagari", canonical_name="IndicSTR12 - Devanagari subset", domain="real_scene_text_devanagari",
  origin="CVIT, IIIT Hyderabad", official_url="https://cvit.iiit.ac.in/research/projects/cvit-projects/indicstr",
  citation="Lunia et al., IndicSTR12, ICDAR 2023 (arXiv:2403.08007)", media_type="image",
  provided_labels="TWO kinds of file, corrected 25 Aug 2026 - see supersedes_note. (a) 375 FULL SCENE PHOTOGRAPHS, each with a per-image *_gt.txt in tab-separated format: region index, 8 polygon coordinates, Unicode transcription - ONE LINE PER TEXT REGION. Photographs carry 1-98 annotated regions each (median 4, mean 7.2, 2,711 regions total). (b) 2,711 PRE-CROPPED single-word images under cropped_images/, whose filenames encode parent photo + region index + the same 8 polygon coordinates, so each crop resolves to exactly one transcription in its parent's *_gt.txt.",
  supersedes_note="SUPERSEDED WORDING, preserved deliberately rather than erased. This record previously read: 'cropped word images with Unicode labels in per-image *_gt.txt'. That was wrong in a specific way: cropped word images do exist and are the majority of the files, but they are NOT the things the *_gt.txt files label. The *_gt.txt files describe the 375 full scene photographs, one line per region. Correction requested by Eval in eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md and independently reverified by Resources against the manifest and the files on disk. See resources/reports/RES-CORRECTION-01-indicstr12-composition.md.",
  human_annotation_type="manual annotation",
  dataset_size_claimed=">27,000 word images across 12 languages; real.zip = 1,382,967,649 bytes; synthetic companion 62,692,393,572 bytes NOT acquired",
  media_acquired_count=3086,
  locally_paired_records=375,
  paired_note="MEDIA ACQUIRED (3,086) is not the same as LOCALLY PAIRED IMAGE+ANNOTATION RECORDS (375, 12.2%). A 'paired record' means a photograph with its own sidecar *_gt.txt present and parsing to at least one region. The remaining 2,711 files are single-word crops with no sidecar file - but they are NOT unlabelled: 2,711 of 2,713 (99.9%) resolve to exactly one transcription by matching the polygon coordinates in their filename against their parent photograph's *_gt.txt. Resources verified this directly. So: 375 multi-region scene records, 2,711 single-word records, 4 unresolved.",
  access_method="public direct download link on the CVIT project page, no login/form. Host honours HTTP 206. robots.txt disallows Joomla system paths but not /images/datasets/.",
  code_license="not_stated", dataset_annotation_license="not_stated",
  underlying_media_rights="not_stated / not_verified. Photographs of real signage; no rights statement on the project page.",
  redistribution_status="not_stated - treat as NOT permitted", commercial_use_status_if_explicit="not_stated",
  terms_access_notes="Member-level range acquisition: transferred 112 MB of a 1.38 GB archive (8.1%); archive never staged on disk, so no full-archive hash is recorded. Selection = the distributor's hindi/ and marathi/ folders, the two Devanagari-script languages, plus their *_gt.txt files. The 62 GB synthetic companion was deliberately not acquired: RES-002 states clean synthetic text alone is insufficient for calibration.",
  version="Devanagari subset, 3,465 of 31,242 real members", status="partial_download",
  reason="Second Devanagari collection, independent of BSTD. NOT independent of IIIT-ILST: both are CVIT / IIIT Hyderabad releases and 173 files are byte-identical across the two (5.6% of this source, 12.4% of IIIT-ILST). Verified by SHA256, see the integrity report."),

 dict(source_id="src_iiit_ilst_devanagari", canonical_name="IIIT-ILST - Devanagari subset", domain="real_scene_text_devanagari",
  origin="CVIT, IIIT Hyderabad", official_url="https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-ilst",
  citation="Mathew, Jain, Jawahar, ICDAR MOCR Workshop 2017 (arXiv:2104.04437)", media_type="image",
  provided_labels="Same two-part structure as IndicSTR12. (a) 176 FULL SCENE PHOTOGRAPHS with a per-image PASCAL-VOC style .xml carrying one <object> per text region - bounding box plus Unicode transcription. 1-64 regions each (median 8, 1,788 regions total). (b) 1,214 pre-cropped single-word images whose filenames encode parent photo + region index + bounding box; 1,210 of 1,215 (99.6%) resolve to exactly one XML transcription. The original wording 'bounding boxes and transcriptions' was accurate but did not distinguish scene photographs from crops.",
  media_acquired_count=1390,
  locally_paired_records=176,
  paired_note="MEDIA ACQUIRED (1,390) is not the same as LOCALLY PAIRED IMAGE+ANNOTATION RECORDS (176, 12.7%). The other 1,214 files are crops that carry no sidecar .xml but resolve to a transcription via the bounding box in their filename.",
  human_annotation_type="manual annotation",
  dataset_size_claimed="~1,000 real images per script across Devanagari/Telugu/Malayalam; IIIT-ILST.zip = 638,566,321 bytes",
  access_method="public direct download link on the CVIT project page, no login/form. Host honours HTTP 206.",
  code_license="not_stated", dataset_annotation_license="not_stated",
  underlying_media_rights="not_stated / not_verified. Photographs of real signage; no rights statement on the project page.",
  redistribution_status="not_stated - treat as NOT permitted", commercial_use_status_if_explicit="not_stated",
  terms_access_notes="OVERLAPS IndicSTR12 - TWO VALID DENOMINATORS, both true, same numerator: (1) 173 of 1,390 ACQUIRED images = 12.4%, the correct figure for the source as a whole; (2) 173 of 176 LOCALLY PAIRED records = 98.3%, the figure a consumer actually feels, because only paired records can be scored. Only 3 paired records are genuinely unique to this source. The overlap sits ENTIRELY in the annotated scene photographs - no cropped word image is byte-identical across the two sources. Further, all 173 shared photographs are exactly IndicSTR12's complete Hindi-labelled scene set (173 of 173), so the smaller dataset's Devanagari scene folder is effectively the larger dataset's Hindi scene folder. CONTENT-LEVEL CAVEAT verified by Resources: 1,205 of this source's 1,214 crops (99.3%) are derived from photographs shared with IndicSTR12. They are not byte-identical, so hash-based deduplication does NOT flag them, but they depict the same regions of the same photographs - relevant to any holdout that assumes crop-level independence. Member-level range acquisition of the distributor's Devanagari/ folder plus README.txt. All 1,569 members verified present at their exact central-directory sizes with matching SHA256. NOTE: the recorded bytes_transferred_total for this source undercounts - a first attempt failed partway with HTTP/2 framing errors from this host and the rerun skipped members already on disk. The figure is left as measured rather than replaced with an estimate; see _transient_acquisition.json.",
  version="Devanagari subset, 1,569 of 4,847 real members", status="partial_download",
  reason="Third Devanagari collection, with a different annotation format (XML boxes+transcriptions). NOT independent of IndicSTR12: 173 of this source's 1,390 items (12.4%) are byte-identical to IndicSTR12 items. Both come from CVIT / IIIT Hyderabad. Independent of BSTD."),

 dict(source_id="src_pvp", canonical_name="Personalized Visual Persuasion (PVP)", domain="persuasion_image_ratings",
  origin="holi-lab / Seoul National University", official_url="https://huggingface.co/datasets/holi-lab/PVP",
  citation="ACL 2025; arXiv:2506.00481", media_type="image",
  provided_labels="9 persuasion strategies, persuasiveness ratings, annotator demographics and psychological traits",
  human_annotation_type="2,521 human annotators", dataset_size_claimed="28,454 images, 596 messages, 20 topics",
  access_method="GATED. HuggingFace API reports gated: auto on holi-lab/PVP - login plus terms acceptance required even though approval is automatic.",
  code_license="MIT (GitHub repository code)", dataset_annotation_license="not_stated",
  underlying_media_rights="not_verified. Paper describes images as partly DALL-E generated and partly sourced via Google Image Search; the web-sourced portion carries third-party copyright with no stated clearance.",
  redistribution_status="not_stated", commercial_use_status_if_explicit="not_stated",
  terms_access_notes="Reassessed under clarification 6/7 and still blocked - the blocker is an ACCESS GATE, which clarification 6 does not waive. Separately checked holi-lab/visual_persuasion (ungated): it contains only faithfulness annotations and train_data JSON, NO images, so it is not the PVP media distribution. Per clarification 2, not substituted. Earlier note retained: a web search asserted the DATASET is MIT-licensed; that is the repository CODE licence and was not accepted.",
  version="n/a", status="blocked_access",
  reason="Gated (login + terms acceptance). Not crossable. Licence silence was never the operative blocker."),

 dict(source_id="src_ava", canonical_name="AVA (Aesthetic Visual Analysis)", domain="real_photography_aesthetics",
  origin="Murray et al., CVPR 2012", official_url="http://www.vabs.info/papers/AVA/",
  citation="Murray, Marchesotti, Perronnin, CVPR 2012", media_type="image",
  provided_labels="aesthetic ratings (~210 per image), 66 semantic labels, 14 style labels",
  human_annotation_type="photo-contest community voting", dataset_size_claimed="~255,000 images",
  access_method="Authors distribute image lists and annotations only - no media. The only routes are scraping dpchallenge.com or an academic torrent.",
  code_license="n/a", dataset_annotation_license="not_stated",
  underlying_media_rights="EXPLICITLY RESERVED. dpchallenge.com states: 'All digital photo copyrights belong to the photographers and may not be used without permission.'",
  redistribution_status="explicitly prohibited by site terms",
  commercial_use_status_if_explicit="not_stated for photographs; reproduction prohibited regardless",
  terms_access_notes="Reassessed under clarification 6/7 and now blocked on STRONGER grounds than before. dpchallenge.com/terms.php explicitly prohibits: 'use a robot, spider or other device or process to monitor the activity on or copy pages from the DPChallenge.com Web Site'; 'You may not reproduce or distribute any information available from the Website, electronically or otherwise. You shall not store or aggregate such information in any manner'; and deep-linking to images. robots.txt does not blanket-disallow (the User-agent:* block is commented out) but the terms of service do. Torrent route remains out of scope.",
  version="n/a", status="blocked_license",
  reason="Explicit site terms prohibit robots, reproduction and aggregation; photographers' copyright expressly reserved. Clarification 6 does not permit proceeding despite an explicit restriction."),

 dict(source_id="src_pitt_ads", canonical_name="Pitt Image and Video Ads", domain="real_advertising",
  origin="Univ. of Pittsburgh, Kovashka group", official_url="https://people.cs.pitt.edu/~kovashka/ads/",
  citation="Hussain et al., CVPR 2017", media_type="image + video",
  provided_labels="topic, sentiment, action-reason Q/A, strategy, symbolism bounding boxes",
  human_annotation_type="crowdworker (Amazon Mechanical Turk)", dataset_size_claimed="64,832 image ads; 3,477 video ads",
  access_method="EMAIL REQUEST GATE. readme_images.txt: 'To obtain the dataset for research purposes, please email us.' Videos supplied as an ID list, not media.",
  code_license="not_stated", dataset_annotation_license="not_stated",
  underlying_media_rights="not_verified. Advertisements collected from the web; third-party brand copyright applies.",
  redistribution_status="not_stated", commercial_use_status_if_explicit="not_stated",
  terms_access_notes="Explicitly kept blocked by clarification 7. An email request is a human permission decision. Annotation zips remain directly downloadable if metadata-only use is ever wanted.",
  version="n/a", status="blocked_access",
  reason="Email/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation."),

 dict(source_id="src_lsvq", canonical_name="LIVE-FB LSVQ", domain="real_social_video_quality",
  origin="LIVE Lab, UT Austin / CU Boulder", official_url="https://www.colorado.edu/lab/live/live-fb-large-scale-social-video-quality-database",
  citation="Ying et al., Patch-VQ, CVPR 2021", media_type="video",
  provided_labels="~5.5M quality scores from ~6,300 subjects", human_annotation_type="subjective quality study",
  dataset_size_claimed="38,811 videos, 116,433 v-patches",
  access_method="FORM GATE. Free to researchers but a download form must be completed.",
  code_license="n/a", dataset_annotation_license="not_stated",
  underlying_media_rights="not_verified. Sampled from Internet Archive and YFCC100M.",
  redistribution_status="not_stated", commercial_use_status_if_explicit="not_stated",
  terms_access_notes="Explicitly kept blocked by clarification 7. Repo also notes the automatic form reply was broken and some videos may no longer be retrievable.",
  version="n/a", status="blocked_access",
  reason="Form/manual-approval gate; clarification 7 keeps this blocked absent separate Controller authorisation."),
]

FIELDS = ["source_id","canonical_name","domain","origin","official_url","citation","media_type",
 "provided_labels","human_annotation_type","dataset_size_claimed","downloaded_item_count",
 "downloaded_bytes","access_method","code_license","dataset_annotation_license",
 "underlying_media_rights","redistribution_status","commercial_use_status_if_explicit",
 "terms_access_notes","version","timestamp","status","reason",
 # optional, added 25 Aug 2026 for the EVAL-003 correction. RES-001 defined these as MINIMUM
 # fields, so extra columns are permitted. Blank where not applicable.
 "media_acquired_count","locally_paired_records","paired_note","supersedes_note"]

for r in S:
    n, b = actual(r["source_id"])
    r["downloaded_item_count"] = n
    r["downloaded_bytes"] = b
    r["timestamp"] = TS

os.makedirs("resources/manifests", exist_ok=True)
os.makedirs("resources/sources", exist_ok=True)
with open("resources/manifests/source-registry-v0.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
    for r in S: w.writerow({k: r.get(k,"") for k in FIELDS})

for r in S:
    md = [f"# Source record — {r['canonical_name']}","",
      f"**source_id:** `{r['source_id']}`  ", f"**status:** `{r['status']}`  ",
      f"**assessed:** {r['timestamp']} (RES-001, under Controller clarifications 6–7)","",
      "## Identity","",
      f"- **Domain:** {r['domain']}", f"- **Origin:** {r['origin']}",
      f"- **Official URL:** {r['official_url']}", f"- **Citation:** {r['citation']}",
      f"- **Media type:** {r['media_type']}", f"- **Claimed size:** {r['dataset_size_claimed']}","",
      "## Labels — source observations, never project ground truth","",
      f"- **Provided labels:** {r['provided_labels']}",
      f"- **Annotation type:** {r['human_annotation_type']}","",
      "## Rights — six separate facts","","| Field | Finding |","|---|---|",
      f"| Code licence | {r['code_license']} |",
      f"| Dataset / annotation licence | {r['dataset_annotation_license']} |",
      f"| Underlying media rights | {r['underlying_media_rights']} |",
      f"| Redistribution status | {r['redistribution_status']} |",
      f"| Access method | {r['access_method']} |",
      f"| Commercial use (if explicit) | {r['commercial_use_status_if_explicit']} |","",
      "## Terms / access notes","", r['terms_access_notes'],"",
      "## Determination","", f"**`{r['status']}`** — {r['reason']}","",
      "## Acquisition state","",
      *( ["**Media acquired is not the same as usable annotated records — read this before sizing any task.**","",
          f"- **Media files acquired:** {r.get('media_acquired_count')}",
          f"- **Locally paired image + sidecar annotation records:** {r.get('locally_paired_records')}",
          "", r.get("paired_note",""), ""] if r.get("locally_paired_records") else [] ),
      *( ["## Correction history","", r["supersedes_note"], ""] if r.get("supersedes_note") else [] ),
      f"- downloaded_item_count (media files): **{r['downloaded_item_count']}**",
      f"- downloaded_bytes: **{r['downloaded_bytes']:,}**",
      f"- version/subset: {r['version']}","",
      "## Permitted use","",
      "Internal research and evaluation only (RES-001 clarification 3). Not redistributable, not",
      "training data, not customer-deliverable, not production-cleared. Rights recorded above as",
      "found; nothing inferred.",""]
    open(f"resources/sources/{r['source_id']}.md","w").write("\n".join(md))

dl = [r for r in S if r["status"] in ("downloaded","partial_download")]
print(f"registry: {len(S)} sources | acquired: {len(dl)} | "
      f"items: {sum(r['downloaded_item_count'] for r in S):,} | "
      f"bytes: {sum(r['downloaded_bytes'] for r in S)/1e9:.2f} GB")
