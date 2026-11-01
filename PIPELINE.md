# Weekly content pipeline — Bioinformatics for Pakistan

Instruction sheet for the automated runs. Read it fully before every run. Owner: Sajad Ahmad (MPhil Bioinformatics, Quaid-e-Azam University).

## Where things go
- **Instagram (@bioinformatics_pakistan): animated Reels only.**
- **LinkedIn page "Bioinformatics for Pakistan": scholarship posters and research/publication news posters only** (no Reels on LinkedIn).

## Weekly plan (all times Asia/Karachi)

| Day | Post | Network | Time |
|---|---|---|---|
| Mon | Animated Reel | Instagram | 10:30 |
| Tue | Scholarship poster | LinkedIn | 17:30 |
| Wed | Animated Reel | Instagram | 10:30 |
| Thu | Research / publication news poster | LinkedIn | 17:30 |
| Fri | Animated Reel | Instagram | 10:30 |

Runs: **Sun 20:41** → Mon Reel + Tue scholarship · **Tue 20:41** → Wed Reel + Thu research news · **Thu 20:41** → Fri Reel.
Before making anything, check Metricool `getScheduledPosts` for the target slot and network; if it's already filled, skip it.
Metricool free plan = 20 posts/month. This plan uses ~21/month (13 Reels + 8 LinkedIn posters). If the planner says no posts are left, skip and report it.

## Accuracy — the most important rule
1. **Never invent, guess or "fill in" anything.** Every name, number, deadline, amount, eligibility rule, finding, author, journal and date must come from a source fetched during the run.
2. Prefer **official pages** (funder, university, government, journal, the institution's press release, PubMed/DOI page). Aggregators may be used to *find* items only; key facts need two independent sources, one official where it can be fetched.
3. **Scholarships:** open to Pakistani citizens, deadline at least 3 weeks away, relevant to biology/bioinformatics/biotech/health/STEM. Official link in the post.
4. **Research news:** a peer-reviewed paper or official institutional announcement from roughly the last 3 weeks, in bioinformatics, genomics, computational biology, biotechnology or biomedical science. Name the journal and link the paper (DOI) or the official release. Say only what the source says: keep qualifiers like "in mice", "early-stage", "preprint" (avoid preprints unless clearly labelled), "may".
5. If anything can't be verified, choose a different item, or skip the post and say why. Never post unverified content.
6. Reels must be scientifically accurate too: well-established science only, no treatment or cure claims, careful wording ("can", "may", "one of the causes").
7. Check `posts_log.md` so nothing repeats.

## Tone — natural, human, not "AI-sounding"
- LinkedIn captions read like a real person sharing something useful: plain sentences, short paragraphs, first-person plural is fine ("Sharing this for anyone applying to…"). **No** hype words ("game-changer", "revolutionary", "unlock", "dive in", "in today's fast-paced world"), no rows of emojis (0–2 max), 3–5 hashtags at the end, a genuine question or prompt to comment is welcome.
- Instagram captions: hook line, 2–3 short paragraphs, save/share line, 10–14 hashtags ending with `#bioinformaticsforpakistan`. Light emoji use.
- **Posters must not all look the same.** Rotate `style=` in `engine/poster.py` (navy, light, forest, plum); don't reuse the previous poster's style. Keep text short; look at the PNG before posting.

## Reels (Instagram)
- Topics: any bioinformatics process or tool, diseases and how they work (especially those common in Pakistan), genetics, genomics, biotechnology, immunology, drug discovery, general science explainers. Disease/health topics perform best (colorectal cancer video: 1,700+ views). Each video a different topic and a different visual theme/accent colour.
- Built with `engine/eng.py` + `engine/vids.py` (full example: `engine/examples/cell.py` + `tts.py`): script lines → Kokoro TTS (`af_heart`, speed ~0.93) → scenes → test frames + contact sheet → sweep all frames for errors → `nohup` render in 2 parallel parts → `audio` → ffmpeg concat + watermark `engine/watermark.png` (`scale=-1:88`, `overlay=W-w-40:128`).
- 55–75 s, 9:16, < 30 MB, `videos/YYYY-MM-DD_slug.mp4`, push, schedule with the raw URL `https://raw.githubusercontent.com/sajadahmad41454/bioinformatics-pakistan-reels/main/videos/<file>`.
- Metricool: network `instagram`, `instagramData: {type: "REEL", showReelOnFeed: true, isAiGenerated: false}`.

## Posters (LinkedIn)
- `engine/poster.py` → `posters/YYYY-MM-DD_slug.png` (1080×1350), kinds `SCHOLARSHIP` / `SCIENCE NEWS`, rotate `style`.
- Metricool: network `linkedin`, `linkedinData: {type: "post", previewIncluded: true}`, media = raw URL of the PNG, alt text describing the poster.

## Metricool common settings
Brand/blogId **7481384**, timezone Asia/Karachi, `autoPublish: true`, `draft: false`. Posts are created the evening before so the owner can review them.

## After each run
Append each post to `posts_log.md` (created, scheduled time, network, type, topic, source URLs). Commit and push.
