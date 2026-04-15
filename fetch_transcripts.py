"""
YouTube Transcript Batch Fetcher
Run this locally — YouTube blocks requests from cloud servers.

Usage:
    pip install youtube-transcript-api
    python3 fetch_transcripts.py

Output: saves one .md file per video into the correct author folder.
"""

import os
import re
from datetime import date

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Run: pip install youtube-transcript-api")
    exit(1)

# ── Add video IDs here ────────────────────────────────────────────────────────
# Format: (author_folder, video_id, video_title, published_date)
VIDEOS = [
    ("nathan-gotch",        "dBKkVMuvkgc", "AI SEO & GEO — The Ultimate Checklist for 2025",         "2025"),
    ("matt-diggity",        "REPLACE_ME",  "Latest Matt Diggity AI SEO Video",                        "2025"),
    ("koray-tugberk-gubur", "REPLACE_ME",  "Topical Authority & Semantic SEO",                        "2025"),
    ("lily-ray",            "REPLACE_ME",  "E-E-A-T and AI Overviews",                                "2025"),
    ("kevin-indig",         "REPLACE_ME",  "Growth Memo — AI Search & GEO",                           "2025"),
    ("aleyda-solis",        "REPLACE_ME",  "Crawling Mondays — AI Crawlers",                          "2025"),
    ("ross-simmonds",       "REPLACE_ME",  "Create Once Distribute Forever",                          "2025"),
    ("jason-barnard",       "REPLACE_ME",  "Answer Engine Optimization",                              "2025"),
    ("ryan-law",            "REPLACE_ME",  "Ahrefs — AI Content That Actually Ranks",                 "2025"),
    ("marie-haynes",        "REPLACE_ME",  "AI Overviews & Algorithm Recovery",                       "2025"),
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
api = YouTubeTranscriptApi()


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fetch_and_save(author, video_id, title, published):
    if video_id == "REPLACE_ME":
        print(f"  SKIP  {author} — no video ID set")
        return

    folder = os.path.join(BASE_DIR, author)
    os.makedirs(folder, exist_ok=True)

    filename = f"{published[:4]}-{slugify(title)[:50]}.md"
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        print(f"  EXISTS {author}/{filename} — skipping")
        return

    print(f"  FETCH  {author} — {video_id}...")
    try:
        transcript = api.fetch(video_id)
        text = " ".join([s.text for s in transcript])

        content = f"""# {title}

- **Author:** {author.replace("-", " ").title()}
- **Video URL:** https://www.youtube.com/watch?v={video_id}
- **Published:** {published}
- **Duration:** [fill in]
- **Date collected:** {date.today().isoformat()}

## Summary

[Fill in after reading transcript]

## Key topics covered

[Fill in after reading transcript]

## Transcript

{text}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  OK     saved {len(text):,} chars → {filename}")

    except Exception as e:
        print(f"  ERROR  {author}: {e}")


if __name__ == "__main__":
    print(f"Fetching {len(VIDEOS)} transcripts...\n")
    for author, vid_id, title, published in VIDEOS:
        fetch_and_save(author, vid_id, title, published)
    print("\nDone.")
