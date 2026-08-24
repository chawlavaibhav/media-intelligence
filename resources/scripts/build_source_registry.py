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
  terms_access_notes="RIGHTS ARE CLEAR - THIS IS A FORMAT BLOCK, NOT A LICENCE BLOCK. The media ship as ONE 13.42 GB videos.zip. There is no addressable per-item path, so a bounded deterministic subset is impossible without partial-archive techniques this pilot should not depend on. Peak requirement (archive + extraction) would be ~26.8 GB against an 8 GB cap and a 12 GB free-space floor.",
  version="n/a", status="too_large_for_pilot",
  reason="Apache-2.0 and ungated, but monolithic 13.42 GB archive cannot be subset. Best candidate for a later, larger acquisition - 12-generator diversity is not available elsewhere."),

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
 "terms_access_notes","version","timestamp","status","reason"]

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
      f"- downloaded_item_count: **{r['downloaded_item_count']}**",
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
