STYLE_PROFILES = {
    "Plain": {
        "description": "Direct, simple explanations.",
        "template": "This matches because it fits the requested mood, genre, or activity."
    },
    "Music Critic": {
        "description": "More analytical, review-like explanations.",
        "template": "This recommendation works because its mood, pacing, and genre cues create a coherent listening situation."
    },
    "Study Companion": {
        "description": "Focused on concentration, calm, and emotional fit.",
        "template": "This fits because it supports the listening task without overwhelming attention."
    },
    "DJ": {
        "description": "Energetic, playlist-oriented explanations.",
        "template": "This belongs in the set because it keeps the energy moving and matches the requested vibe."
    }
}


def generate_specialized_reason(song, user_input, contexts, style="Plain"):
    profile = STYLE_PROFILES.get(style, STYLE_PROFILES["Plain"])
    context_guidance = " ".join(context["guidance"] for context in contexts)

    if style == "Music Critic":
        return (
            f"{profile['template']} {song['title']} by {song['artist']} carries "
            f"{song['mood']} qualities in a {song['genre']} frame. Context used: {context_guidance}"
        )

    if style == "Study Companion":
        return (
            f"{profile['template']} {song['title']} has {song['energy']} energy and "
            f"works for {song['activity']}. Context used: {context_guidance}"
        )

    if style == "DJ":
        return (
            f"{profile['template']} {song['title']} brings {song['energy']} energy, "
            f"making it useful for {song['activity']}. Context used: {context_guidance}"
        )

    return (
        f"{song['title']} matches your request because it connects to "
        f"{song['mood']} moods and works for {song['activity']}."
    )


def compare_specialized_to_baseline(song, user_input, contexts, style):
    baseline = generate_specialized_reason(song, user_input, contexts, style="Plain")
    specialized = generate_specialized_reason(song, user_input, contexts, style=style)

    return {
        "baseline": baseline,
        "specialized": specialized,
        "changed": baseline != specialized,
        "baseline_length": len(baseline.split()),
        "specialized_length": len(specialized.split())
    }
