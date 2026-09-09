# Blind judging - aud-lip (lipsync, Kling lipsync audio-to-video on the accepted lobby clip)

Five clips P01-P05 (the sixth trial was refused by fal on balance). One line per clip: accept or reject plus a note.

Missing: AUD-LIP-03__kling-lipsync-a2v__chain__r1 (fal refused: HTTP 403 'User is locked. Reason: Exhausted balance' - no artifact, infra failure, not a model failure)

## AUD-LIP-01
- ACCEPT only if the man's mouth opens and closes with the syllables of "इस दवाई से मेरी फसल दोगुनी हुई" — a first-language Hindi judge sees the words being spoken; REJECT if the mouth moves out of time by a visible beat.
- ACCEPT only if his lips are closed or at rest during the silence after the line.
- REJECT if the face changes identity, the mouth region shows a visible patch, blur, colour seam or flicker, or the background changes.
- REJECT if the audio in the output is not the supplied voice (re-synthesised, clipped or shifted).

## AUD-LIP-02
- ACCEPT only if the mouth follows the whole line "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." in time — including the English words — with no visible lag or lead.
- ACCEPT only if the lips rest closed during the pauses and after the line.
- REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.
- REJECT if the output audio is not the supplied voice.

## AUD-LIP-03
- ACCEPT only if the mouth follows "Zero petrol. Zero noise. All city." in time, sentence by sentence.
- ACCEPT only if the lips are closed in each of the two pauses and after the last sentence.
- REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.
- REJECT if the output audio is not the supplied voice.
