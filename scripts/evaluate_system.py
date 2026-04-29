import os
import sys

sys.path.insert(0, os.path.abspath("src"))

from agent import run_agentic_recommender


TEST_CASES = [
    {
        "input": "dreamy sad songs for studying",
        "style": "Study Companion",
        "expected_status": "success"
    },
    {
        "input": "chaotic workout music",
        "style": "DJ",
        "expected_status": "success"
    },
    {
        "input": "night walking dreamy electronic",
        "style": "Music Critic",
        "expected_status": "success"
    },
    {
        "input": "recommend something",
        "style": "Plain",
        "expected_status": "rejected"
    }
]


def run_evaluation():
    passed = 0
    total = len(TEST_CASES)
    confidence_scores = []

    print("AI Music Recommender Full Extension Evaluation")
    print("=" * 55)

    for index, case in enumerate(TEST_CASES, start=1):
        result = run_agentic_recommender(case["input"], style=case["style"])
        confidence_scores.append(result["confidence"])

        has_trace = len(result["trace"]) > 0
        has_rag_measurement = result["rag_comparison"] is not None or result["status"] == "rejected"
        has_specialization = (
            result["specialization_comparison"] is not None
            or result["status"] == "rejected"
        )

        success = (
            result["status"] == case["expected_status"]
            and has_trace
            and has_rag_measurement
            and has_specialization
        )

        if success:
            passed += 1
            label = "PASS"
        else:
            label = "FAIL"

        print(f"\nTest {index}: {label}")
        print(f"Input: {case['input']}")
        print(f"Style: {case['style']}")
        print(f"Status: {result['status']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Recommendations: {[rec['title'] for rec in result['recommendations']]}")
        print(f"Trace steps: {[step['step'] for step in result['trace']]}")
        print(f"RAG comparison: {result['rag_comparison']}")
        print(f"Specialization comparison exists: {result['specialization_comparison'] is not None}")

    average_confidence = round(sum(confidence_scores) / len(confidence_scores), 2)

    print("\n" + "=" * 55)
    print(f"Summary: {passed} out of {total} tests passed.")
    print(f"Average confidence score: {average_confidence}")

    if passed == total:
        print("Result: All extension checks passed.")
    else:
        print("Result: Some extension checks failed.")


if __name__ == "__main__":
    run_evaluation()
