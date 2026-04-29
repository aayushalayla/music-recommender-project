def calculate_confidence(user_input, retrieved_songs):
    """
    Returns a confidence score from 0 to 1 based on input quality
    and number of retrieved songs.
    """

    if not user_input or len(user_input.strip()) < 5:
        return 0.0

    if not retrieved_songs:
        return 0.2

    score = 0.4

    if len(retrieved_songs) >= 3:
        score += 0.3
    elif len(retrieved_songs) >= 1:
        score += 0.15

    useful_keywords = [
        "sad", "happy", "angry", "dreamy", "energetic",
        "study", "workout", "walking", "party", "calm",
        "pop", "rap", "indie", "rock", "electronic",
        "chaotic", "quiet", "fast"
    ]

    if any(word in user_input.lower() for word in useful_keywords):
        score += 0.3

    return min(round(score, 2), 1.0)


def validate_recommendations(recommendations, retrieved_songs):
    """
    Checks whether recommendations came from retrieved songs.
    This prevents unsupported recommendations.
    """

    retrieved_titles = [song["title"] for song in retrieved_songs]

    for rec in recommendations:
        if rec["title"] not in retrieved_titles:
            return False

    return True
