try:
    from guardrails import validate_user_input
    from evaluator import calculate_confidence, validate_recommendations
    from retriever import retrieve_multi_source_context, compare_baseline_vs_enhanced
    from specializer import generate_specialized_reason, compare_specialized_to_baseline
except ImportError:
    from src.guardrails import validate_user_input
    from src.evaluator import calculate_confidence, validate_recommendations
    from src.retriever import retrieve_multi_source_context, compare_baseline_vs_enhanced
    from src.specializer import generate_specialized_reason, compare_specialized_to_baseline


def run_agentic_recommender(user_input, style="Plain"):
    """
    Agentic workflow:
    1. Validate input.
    2. Retrieve from multiple sources.
    3. Generate recommendations.
    4. Validate recommendations.
    5. Score confidence.
    6. Return an observable trace.
    """

    trace = []

    valid, message = validate_user_input(user_input)
    trace.append({
        "step": "Guardrail Check",
        "action": "Validate whether the user request is specific enough.",
        "result": message
    })

    if not valid:
        return {
            "status": "rejected",
            "message": message,
            "recommendations": [],
            "confidence": 0.2,
            "trace": trace,
            "rag_comparison": None,
            "specialization_comparison": None
        }

    retrieved = retrieve_multi_source_context(user_input)
    songs = retrieved["songs"]
    contexts = retrieved["contexts"]

    trace.append({
        "step": "Multi-Source Retrieval",
        "action": "Retrieve matching songs and listening-context guidance.",
        "result": {
            "songs": [song["title"] for song in songs],
            "contexts": [context["context"] for context in contexts],
            "source_count": retrieved["source_count"]
        }
    })

    rag_comparison = compare_baseline_vs_enhanced(user_input)
    trace.append({
        "step": "RAG Enhancement Check",
        "action": "Compare song-only retrieval with multi-source retrieval.",
        "result": rag_comparison
    })

    recommendations = []
    for song in songs:
        recommendations.append({
            "title": song["title"],
            "artist": song["artist"],
            "reason": generate_specialized_reason(song, user_input, contexts, style)
        })

    trace.append({
        "step": "Specialized Recommendation Generation",
        "action": f"Generate recommendations using the '{style}' style profile.",
        "result": [rec["title"] for rec in recommendations]
    })

    valid_recommendations = validate_recommendations(recommendations, songs)
    confidence = calculate_confidence(user_input, songs)

    trace.append({
        "step": "Validation and Confidence Scoring",
        "action": "Check that recommendations came from retrieved songs and assign confidence.",
        "result": {
            "recommendations_valid": valid_recommendations,
            "confidence": confidence
        }
    })

    specialization_comparison = None
    if songs:
        specialization_comparison = compare_specialized_to_baseline(
            songs[0], user_input, contexts, style
        )

    if not songs:
        return {
            "status": "no_matches",
            "message": "No strong matches found. Try a different mood, genre, or activity.",
            "recommendations": [],
            "confidence": confidence,
            "trace": trace,
            "rag_comparison": rag_comparison,
            "specialization_comparison": specialization_comparison
        }

    return {
        "status": "success",
        "message": "Recommendations generated.",
        "recommendations": recommendations,
        "confidence": confidence,
        "trace": trace,
        "rag_comparison": rag_comparison,
        "specialization_comparison": specialization_comparison
    }
