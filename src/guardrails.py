def validate_user_input(user_input):
    """
    Checks whether the user's request is specific enough
    to generate useful recommendations.
    """

    if not user_input or not user_input.strip():
        return False, "Input cannot be empty. Add a mood, genre, or activity."

    if len(user_input.strip()) < 5:
        return False, "Input is too vague. Add a mood, genre, or activity."

    vague_inputs = [
        "recommend something",
        "music",
        "songs",
        "anything",
        "whatever"
    ]

    if user_input.strip().lower() in vague_inputs:
        return False, "Please include a mood, activity, genre, or situation."

    return True, "Input accepted."
