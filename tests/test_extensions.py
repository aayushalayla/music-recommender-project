from src.agent import run_agentic_recommender
from src.retriever import compare_baseline_vs_enhanced
from src.specializer import compare_specialized_to_baseline


def test_agent_trace_exists():
    result = run_agentic_recommender("dreamy sad songs for studying", style="Study Companion")
    assert result["status"] == "success"
    assert len(result["trace"]) >= 4


def test_rag_enhancement_adds_context_source():
    comparison = compare_baseline_vs_enhanced("dreamy sad songs for studying")
    assert comparison["added_context_sources"] >= 1
    assert comparison["enhanced_score"] >= comparison["baseline_score"]


def test_specialized_output_differs_from_baseline():
    song = {
        "title": "Space Song",
        "artist": "Beach House",
        "mood": "dreamy sad calm",
        "genre": "indie",
        "activity": "studying walking",
        "energy": "medium"
    }

    contexts = [
        {
            "context": "studying",
            "keywords": "study focus",
            "guidance": "Prefer songs with low or medium energy."
        }
    ]

    comparison = compare_specialized_to_baseline(
        song,
        "dreamy sad songs for studying",
        contexts,
        "Music Critic"
    )

    assert comparison["changed"] is True
    assert comparison["specialized_length"] != comparison["baseline_length"]


def test_guardrail_rejects_vague_input_through_agent():
    result = run_agentic_recommender("recommend something", style="Plain")
    assert result["status"] == "rejected"
    assert result["confidence"] <= 0.2
