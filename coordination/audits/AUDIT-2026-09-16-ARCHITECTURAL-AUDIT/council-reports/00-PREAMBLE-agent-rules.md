SHARED PREAMBLE FOR ALL AUDIT AGENTS (read fully)

You are one council in an independent READ-ONLY architectural audit of the Media Intelligence programme.
Repos on disk (all already cloned; do NOT clone again):
  MI  = /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence      (main @ 3bb9a3c3da484e43d4d54ae20543d1d246769ac6 — verify with git rev-parse HEAD)
  MF  = /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-factory           (predecessor; checked-out branch spike/media-generation-tests @ 57b2cca; origin/main @ 7279ec5)
  MFH = /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-factory-controller-handoff  (non-git evidence bundle extracted from MF)
  UP  = /Users/vaibhavchawla/Vaibhav_Personal_Projects/upwork-project          (commercial proposition; main @ ff06dab)
  UPT = /Users/vaibhavchawla/Vaibhav_Personal_Projects/upwork-portfolio-tiles  (published portfolio tiles, git, local)
  UPM = /Users/vaibhavchawla/Vaibhav_Personal_Projects/upwork-portfolio-media  (portfolio media, non-git)
  Prior independent reviews (28 Aug 2026, local only): /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-os-review.md and media-intelligence-project-head-review.md
Key MI refs: PR #103 branch work/agency-sync-2026-09-16 head 1de2b37; Cumin raw job branch work/agency-job-cuminco-chopsticks-001, immutable evidence commit de1f978 (branch head is now 1aea4d2, one sync commit later);
  Upwork intro raw branch work/pilot-upwork-intro-video-v4; portfolio raw branch work/upwork-portfolio-samples-2026-09-15.
  MI has many git worktrees (git worktree list) — you may READ them but never modify them.

HARD RULES
- READ-ONLY. Do not edit, create, delete, commit, checkout, switch, stash, or reset anything inside any repo or worktree. Do not run `git checkout`/`git switch` in any repo.
  To read a file from another branch use `git show <ref>:<path>` or `git archive <ref> <path> | tar -x -C <scratch>`.
- Never call any AI/media provider, never spend money, never run anything that dispatches network generation. Local python/ffmpeg/ffprobe/grep on committed bytes is fine.
- Write ONLY under your scratch directory: /private/tmp/claude-501/-Users-vaibhavchawla-Vaibhav-Personal-Projects-media-intelligence/d54000da-a4e6-4d41-b5b8-32d2b70cd318/scratchpad/audit/
- PROJECT-MEMORY.md and coordination/CONTROL-STATE.md are MAPS, not truth; reconcile every important claim against git history, decision records and artifacts. Do not use them as evidence when the underlying artifact contradicts them.
- Do not redesign the product. Return EVIDENCE for your bounded questions. Recommendations only where asked, clearly marked.

EVIDENCE STANDARD
- Repository claims: cite `path @ short-sha` (+ line range where possible). Branch material: `branch @ sha : path`. Media: path + sha256 where cheap.
- Label every important statement: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN.
- Report counts you actually computed (show the command) rather than counts you read in prose.
- When two sources conflict, report the conflict; never harmonise silently.
- Distinguish these eight states and say which one you can actually prove: knowledge exists → was retrieved → entered context → model understood it → it changed a decision → the decision was correct → survived production → QA detected failure.

OUTPUT
- Write your full report (as long as needed, markdown, with a "Findings ranked" section and an "Open questions / unknowns" section) to the file named in your task.
- Return to the lead a summary of at most 700 words: top findings (with the strongest citations), the file path, and anything the lead must know that you could not resolve.
