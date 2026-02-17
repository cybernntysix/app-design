"""Terminal-only dashboard preview for environments without Kivy.

This script mirrors the key dashboard sections and sample data so contributors
can quickly validate content/layout intent when GUI dependencies are unavailable.
"""

from __future__ import annotations

import argparse
from textwrap import shorten

SONG_DATA = {
    "YouTube": [("Dreams", 70000, 210), ("Legacy", 30000, 90), ("Violet Skies", 20000, 60)],
    "Spotify": [("Dreams", 60000, 180), ("Legacy", 25000, 75), ("Violet Skies", 10000, 30)],
    "SoundCloud": [("Dreams", 20000, 40), ("Legacy", 15000, 30), ("Violet Skies", 5000, 10)],
}


def total_revenue() -> int:
    return sum(royalty for songs in SONG_DATA.values() for _, _, royalty in songs)


def get_matches(query: str) -> list[tuple[str, str, int, int]]:
    query = query.strip().lower()
    rows: list[tuple[str, str, int, int]] = []
    for platform, songs in SONG_DATA.items():
        for title, streams, revenue in songs:
            if query and query not in f"{title} {platform}".lower():
                continue
            rows.append((platform, title, streams, revenue))
    rows.sort(key=lambda item: item[3], reverse=True)
    return rows


def hline(width: int = 80) -> str:
    return "=" * width


def section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def render_preview(artist_name: str, query: str, platform: str) -> None:
    print(hline())
    print(shorten(f"Welcome back, {artist_name}. Momentum is strong this week.", width=78, placeholder="…"))
    print("Next milestone: Reach $1,500 in monthly royalties (86% complete)")
    print(hline())

    section("Metrics")
    print(f"Total revenue      : ${total_revenue():,}")
    print("Top-earning song   : Dreams ($500)")
    print("Top platform       : YouTube ($600)")
    print("Opportunities      : Register 2 songs")

    section(f"Chart data ({platform})")
    songs = sorted(SONG_DATA[platform], key=lambda row: row[1], reverse=True)
    for idx, (title, streams, revenue) in enumerate(songs, start=1):
        print(f"{idx}. {title:<14} streams={streams:>7,}  royalties=${revenue:<4}")

    section(f"Song insights (query={query!r})")
    matches = get_matches(query)
    if not matches:
        print("No songs match your search yet.")
    else:
        for platform_name, title, streams, revenue in matches[:6]:
            print(f"{platform_name:<10} | {title:<14} | {streams:>7,} streams | ${revenue:<4}")

    section("News")
    print("Genius            : Top 10 Lyrics of the Week")
    print("Lyrical Lemonade  : New Visuals: Rising Artists to Watch")
    print("Rolling Stone     : Indie Artists Breaking Out in 2025")
    print("Billboard         : Streaming Trends: Hip Hop & Beyond")
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a text dashboard preview without Kivy.")
    parser.add_argument("--artist", default="Artist", help="Artist name shown in preview header.")
    parser.add_argument("--query", default="", help="Search filter for song insights.")
    parser.add_argument(
        "--platform",
        default="YouTube",
        choices=sorted(SONG_DATA),
        help="Platform dataset to display in chart section.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    render_preview(args.artist, args.query, args.platform)
