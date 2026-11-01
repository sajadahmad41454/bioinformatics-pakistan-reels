# Weekly content pipeline — @bioinformatics_pakistan

This file is the instruction sheet for the automated runs. Read it fully before every run.

## Weekly plan (all times Asia/Karachi)

| Day | Post | Type | Time |
|---|---|---|---|
| Mon | Animated Reel (disease / bioinformatics topic) | REEL | 10:30 |
| Tue | Scholarship poster (verified, open, fully/mostly funded) | Image POST | 17:30 |
| Wed | Animated Reel | REEL | 10:30 |
| Thu | Science-news poster (real discovery from the last ~2 weeks) | Image POST | 17:30 |
| Fri | Animated Reel | REEL | 10:30 |

Runs: **Sun 20:41** → Mon Reel + Tue scholarship · **Tue 20:41** → Wed Reel + Thu news · **Thu 20:41** → Fri Reel.

## Hard rules for information posts (scholarships, discoveries)
1. **Never invent anything.** Every fact (name, deadline, coverage, eligibility, finding, journal) must come from a source fetched during the run.
2. Prefer the **official page** (university, funder, government, journal, or the institution's own press release). Aggregator sites (scholars4dev, opportunitiesforafricans, propakistani, etc.) may be used to *find* items, but key facts must be confirmed by at least two independent sources, one official when it can be fetched.
3. Scholarships: deadline must be **at least 3 weeks in the future**, open to Pakistani citizens, relevant to science/biology/bioinformatics/health/STEM students. Put the official link in the caption. If any key fact cannot be confirmed, pick a different scholarship.
4. Science news: must be a peer-reviewed paper or an official announcement from a recognised institution (Nature, Science, Cell, NEJM, Lancet, eLife, NIH, WHO, EMBL-EBI, university press office…), published in the last ~3 weeks. Caption names the journal/institution and links to it. No hype, no claims beyond what the source says ("may", "in mice", "early-stage" where true).
5. If nothing qualifies, skip that post and say so in the log — never post something unverified.
6. Check `posts_log.md` so nothing is repeated.

## Reels
- Built with `engine/eng.py` + `engine/vids.py` (see `engine/examples/cell.py` and `tts.py` for a complete example: script lines → Kokoro TTS → scenes → `render` → `audio` → ffmpeg concat + watermark).
- 55–75 s, 9:16, narrated (Kokoro `af_heart`, speed ~0.93), original animation, watermark `engine/watermark.png` at top-right (`scale=-1:88`, `overlay=W-w-40:128`).
- Topics: disease mechanisms (especially ones common in Pakistan), genetics, genomics, bioinformatics methods, drug discovery. Disease topics perform best. Scientifically accurate, no treatment claims, no fear-mongering. Each video a different visual theme/accent colour.
- Render in background with `nohup` + 2 parallel parts; verify every frame renders (sweep) before full render; check a contact sheet visually.
- Save to `videos/YYYY-MM-DD_slug.mp4` (< 30 MB), push, then schedule with the raw URL:
  `https://raw.githubusercontent.com/sajadahmad41454/bioinformatics-pakistan-reels/main/videos/<file>`
- `isAiGenerated: false` (original animation).

## Posters
- `engine/poster.py` → `posters/YYYY-MM-DD_slug.png` (1080×1350). Kinds: `SCHOLARSHIP`, `SCIENCE NEWS`.
- Look at the rendered PNG before scheduling (no overlapping text).

## Metricool
- Brand/blogId **7481384**, timezone Asia/Karachi, network `instagram`.
- Reel: `instagramData: {type: "REEL", showReelOnFeed: true, isAiGenerated: false}`. Poster: `type: "POST"`.
- `autoPublish: true`, `draft: false` (posts are created ~14–20 h ahead so the owner can review/edit in Metricool).
- Captions: hook line, 2–4 short paragraphs, call to action (save/share), 10–14 hashtags ending with `#bioinformaticsforpakistan`. For info posts the official link goes in the caption.

## After each run
Append to `posts_log.md`: date, post type, topic, scheduled time, sources used. Commit and push.
