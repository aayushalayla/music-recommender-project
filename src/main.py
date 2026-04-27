"""
Command line runner for the Music Recommender Simulation.

Demonstrates all four challenges:
  Challenge 1 — Advanced features (popularity, decade, sub_mood, liveness, language)
  Challenge 2 — Multiple scoring modes (balanced / genre_first / mood_first / energy_focused)
  Challenge 3 — Diversity penalty (greedy reranker prevents artist/genre repeats)
  Challenge 4 — Visual summary table via tabulate (ASCII fallback if not installed)
"""

try:
    from .recommender import load_songs, recommend_songs, SCORING_MODES
except ImportError:
    from recommender import load_songs, recommend_songs, SCORING_MODES

try:
    from tabulate import tabulate
    _HAS_TABULATE = True
except ImportError:
    _HAS_TABULATE = False


# --------------------------------------------------------------------------
# Challenge 4 — Visual output helpers
# ---------------------------------------------------------------------------

def _truncate(text: str, max_len: int = 38) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def format_table(recommendations: list, profile_name: str,
                 mode: str, diversity: bool) -> str:
    """
    Challenge 4: render recommendations as a formatted table.

    Uses tabulate when available; falls back to a hand-drawn ASCII box.
    The 'Why' column always shows the scoring reasons so it's clear how each
    song earned its score.
    """
    if not recommendations:
        return "  No recommendations found.\n"

    headers = ["#", "Title", "Artist", "Genre", "Mood", "Score", "Why this match"]
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        rows.append([
            rank,
            _truncate(song.get("title", "?"), 22),
            _truncate(song.get("artist", "?"), 18),
            song.get("genre", "?"),
            song.get("mood", "?"),
            f"{score:.2f}",
            _truncate(explanation, 55),
        ])

    mode_label = mode.replace("_", " ").title()
    diversity_label = "  [diversity ON]" if diversity else ""
    header_line = (
        f"  Profile : {profile_name}\n"
        f"  Mode    : {mode_label}{diversity_label}\n"
    )

    if _HAS_TABULATE:
        table = tabulate(rows, headers=headers, tablefmt="rounded_outline",
                         colalign=("right", "left", "left", "left",
                                   "left", "right", "left"))
    else:
        # Minimal ASCII fallback
        col_widths = [max(len(str(r[i])) for r in [headers] + rows)
                      for i in range(len(headers))]
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        def fmt_row(r):
            return "|" + "|".join(
                f" {str(r[i]).ljust(col_widths[i])} " for i in range(len(r))
            ) + "|"
        lines = [sep, fmt_row(headers), sep]
        for r in rows:
            lines.append(fmt_row(r))
        lines.append(sep)
        table = "\n".join(lines)

    return header_line + table + "\n"


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------
# Each profile shows off a different combination of:
#   • base preferences  (genre / mood / energy)
#   • advanced features (popularity_target / preferred_decade / sub_mood /
#                        preferred_liveness / preferred_language)
#   • scoring mode      (balanced / genre_first / mood_first / energy_focused)
#   • diversity flag
# ---------------------------------------------------------------------------

USER_PROFILES = {
    # --- Original five profiles (Challenge 1: advanced fields added) ------

    "High-Energy Pop": {
        "description": "Upbeat, high-energy pop lover who wants trendy recent hits",
        "prefs": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "euphoric",   # rewards euphoric sub-mood
            "popularity_target": 75.0,          # wants popular songs (75/100)
            "preferred_decade": 2020,           # only interested in 2020s tracks
            "scoring_mode": "balanced",
        },
        "diversity": False,
    },

    "Chill Lofi": {
        "description": "Focus/study vibes, relaxed atmosphere, studio-polished",
        "prefs": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "dreamy",
            "preferred_liveness": 0.1,          # wants clean studio recordings
            "preferred_decade": 2020,
            "scoring_mode": "mood_first",       # Challenge 2: mood over genre
        },
        "diversity": False,
    },

    "Deep Intense Rock": {
        "description": "High-energy rock fan, intense moods, raw live feel",
        "prefs": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "aggressive",
            "preferred_liveness": 0.5,          # likes live, raw recordings
            "preferred_decade": 2010,
            "scoring_mode": "genre_first",      # Challenge 2: genre loyalty
        },
        "diversity": True,                      # Challenge 3: no artist repeats
    },

    "Smooth Jazz": {
        "description": "Sophisticated relaxed listening, mellow studio sound",
        "prefs": {
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.37,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "romantic",
            "preferred_liveness": 0.35,
            "popularity_target": 55.0,          # prefers lesser-known artists
            "scoring_mode": "energy_focused",   # Challenge 2: energy-focused
        },
        "diversity": False,
    },

    "Energetic Electronic": {
        "description": "Upbeat electronic for active moments, loves mainstream",
        "prefs": {
            "genre": "electronic",
            "mood": "energetic",
            "energy": 0.95,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "euphoric",
            "popularity_target": 80.0,
            "preferred_decade": 2020,
            "scoring_mode": "balanced",
        },
        "diversity": True,                      # Challenge 3: genre variety
    },

    # --- Two extra profiles demonstrating mode/diversity contrasts --------

    "Nostalgic Acoustic": {
        "description": "2000s nostalgia trip, loves raw acoustic recordings",
        "prefs": {
            "genre": "folk",
            "mood": "peaceful",
            "energy": 0.4,
            # Challenge 1 advanced fields
            "preferred_sub_mood": "nostalgic",
            "preferred_decade": 2000,           # wants 2000s-era tracks
            "preferred_liveness": 0.65,         # appreciates that live feel
            "popularity_target": 50.0,          # underground / indie
            "scoring_mode": "mood_first",       # emotional feel first
        },
        "diversity": True,
    },

    "Mainstream Energy Mix": {
        "description": "Anything high-energy and popular — genre doesn't matter",
        "prefs": {
            "genre": "electronic",
            "mood": "energetic",
            "energy": 0.9,
            # Challenge 1 advanced fields
            "popularity_target": 85.0,          # only mainstream hits
            "preferred_decade": 2020,
            "scoring_mode": "energy_focused",   # Challenge 2: energy-only ranking
        },
        "diversity": True,                      # Challenge 3: force variety
    },
}


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    # Print mode legend once at the top
    print("\n" + "=" * 72)
    print("  VIBEMATH 1.0 — MUSIC RECOMMENDER SIMULATION")
    print("=" * 72)
    print("\n  SCORING MODES available:")
    for name, w in SCORING_MODES.items():
        print(f"    {name:<16} genre={w['genre']}  mood={w['mood']}  energy={w['energy']}")
    print()

    for profile_name, profile_data in USER_PROFILES.items():
        prefs       = profile_data["prefs"]
        diversity   = profile_data.get("diversity", False)
        mode        = prefs.get("scoring_mode", "balanced")
        description = profile_data["description"]

        # Print a compact preference summary
        print("─" * 72)
        print(f"  {profile_name}  |  {description}")
        adv = []
        if prefs.get("preferred_sub_mood"):
            adv.append(f"sub_mood={prefs['preferred_sub_mood']}")
        if prefs.get("popularity_target", -1) >= 0:
            adv.append(f"popularity≈{int(prefs['popularity_target'])}")
        if prefs.get("preferred_decade", 0):
            adv.append(f"decade={prefs['preferred_decade']}s")
        if prefs.get("preferred_liveness", -1) >= 0:
            adv.append(f"liveness≈{prefs['preferred_liveness']}")
        print(f"  genre={prefs['genre']}  mood={prefs['mood']}  "
              f"energy={prefs['energy']}  " + "  ".join(adv))

        recs = recommend_songs(prefs, songs, k=5, mode=mode, diversity=diversity)
        print(format_table(recs, profile_name, mode, diversity))


if __name__ == "__main__":
    main()
