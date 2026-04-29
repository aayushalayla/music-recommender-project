import pandas as pd


SONG_DATA_PATH = "data/songs.csv"
CONTEXT_DATA_PATH = "data/listening_contexts.csv"


def _tokenize(text):
    return set(str(text).lower().replace(",", " ").split())


def load_songs(path=SONG_DATA_PATH):
    return pd.read_csv(path).fillna("").to_dict(orient="records")


def load_contexts(path=CONTEXT_DATA_PATH):
    return pd.read_csv(path).fillna("").to_dict(orient="records")


def retrieve_songs(user_input, top_k=3):
    """
    Retrieves songs from a custom song dataset.
    This is the base retrieval layer.
    """
    songs = load_songs()
    query_words = _tokenize(user_input)
    scored = []

    for song in songs:
        searchable_text = " ".join(str(value) for value in song.values())
        song_words = _tokenize(searchable_text)
        score = len(query_words.intersection(song_words))

        if score > 0:
            scored.append((score, song))

    scored.sort(reverse=True, key=lambda item: item[0])
    return [song for score, song in scored[:top_k]]


def retrieve_contexts(user_input, top_k=2):
    """
    Retrieves listening-context guidance from a second data source.
    This is the RAG enhancement: the system uses multiple sources,
    not just a song list.
    """
    contexts = load_contexts()
    query_words = _tokenize(user_input)
    scored = []

    for context in contexts:
        searchable_text = f"{context['context']} {context['keywords']} {context['guidance']}"
        context_words = _tokenize(searchable_text)
        score = len(query_words.intersection(context_words))

        if score > 0:
            scored.append((score, context))

    scored.sort(reverse=True, key=lambda item: item[0])
    return [context for score, context in scored[:top_k]]


def retrieve_multi_source_context(user_input):
    """
    Returns both song matches and listening-context matches.
    The recommendation generator uses both sources.
    """
    songs = retrieve_songs(user_input)
    contexts = retrieve_contexts(user_input)

    return {
        "songs": songs,
        "contexts": contexts,
        "source_count": int(bool(songs)) + int(bool(contexts))
    }


def compare_baseline_vs_enhanced(user_input):
    """
    Measures whether multi-source retrieval improves the system.
    Baseline = song retrieval only.
    Enhanced = song retrieval + context guidance retrieval.
    """
    baseline_songs = retrieve_songs(user_input)
    enhanced = retrieve_multi_source_context(user_input)

    baseline_score = len(baseline_songs)
    enhanced_score = len(enhanced["songs"]) + len(enhanced["contexts"])

    return {
        "baseline_score": baseline_score,
        "enhanced_score": enhanced_score,
        "improved": enhanced_score > baseline_score,
        "added_context_sources": len(enhanced["contexts"])
    }
