import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from guardrails import validate_user_input
from evaluator import calculate_confidence, validate_recommendations


SONGS = [
    {
        "title": "Space Song",
        "artist": "Beach House",
        "mood": "dreamy sad calm",
        "genre": "indie",
        "activity": "studying walking"
    },
    {
        "title": "Moon Song",
        "artist": "Phoebe Bridgers",
        "mood": "sad soft reflective",
        "genre": "indie",
        "activity": "studying crying walking"
    },
    {
        "title": "Fourth of July",
        "artist": "Sufjan Stevens",
        "mood": "sad quiet emotional",
        "genre": "folk indie",
        "activity": "studying reflection"
    },
    {
        "title": "212",
        "artist": "Azealia Banks",
        "mood": "chaotic energetic aggressive",
        "genre": "rap electronic",
        "activity": "workout party"
    },
    {
        "title": "Heads Will Roll",
        "artist": "Yeah Yeah Yeahs",
        "mood": "energetic dark dance",
        "genre": "rock electronic",
        "activity": "workout party"
    },
    {
        "title": "B.O.B.",
        "artist": "OutKast",
        "mood": "chaotic fast energetic",
        "genre": "rap",
        "activity": "workout running"
    }
]


TEST_CASES = [
    {
        "input": "dreamy sad songs for studying",
        "should_pass": True,
        "expected_keyword": "sad"
    },
    {
        "input": "chaotic workout music",
        "should_pass": True,
        "expected_keyword": "workout"
    },
    {
        "input": "recommend something",
        "should_pass": False,
        "expected_keyword": None
    },
    {
        "input": "",
        "should_pass": False,
        "expected_keyword": None
    }
]


def retrieve_songs(user_input, songs=SONGS):
    query_words = set(user_input.lower().split())
    scored = []

    for song in songs:
        searchable_text = " ".join([
            song["title"],
            song["artist"],
            song["mood"],
            song["genre"],
            song["activity"]
        ]).lower()

        score = sum(1 for word in query_words if word in searchable_text)

        if score > 0:
            scored.append((score, song))

    scored.sort(reverse=True, key=lambda item: item[0])
    return [song for score, song in scored[:3]]


def generate_recommendations(retrieved_songs):
    return [
        {
            "title": song["title"],
            "artist": song["artist"]
        }
        for song in retrieved_songs
    ]


def run_evaluation():
    passed = 0
    total = len(TEST_CASES)
    confidence_scores = []

    print("AI Music Recommender Evaluation")
    print("=" * 40)

    for index, case in enumerate(TEST_CASES, start=1):
        user_input = case["input"]
        valid, message = validate_user_input(user_input)

        if not valid:
            confidence = calculate_confidence(user_input, [])
            success = case["should_pass"] is False
            retrieved_songs = []
            recommendations = []
        else:
            retrieved_songs = retrieve_songs(user_input)
            recommendations = generate_recommendations(retrieved_songs)
            confidence = calculate_confidence(user_input, retrieved_songs)
            valid_recs = validate_recommendations(recommendations, retrieved_songs)

            keyword_match = True
            if case["expected_keyword"]:
                keyword_match = any(
                    case["expected_keyword"] in " ".join(song.values()).lower()
                    for song in retrieved_songs
                )

            success = (
                case["should_pass"] is True
                and len(retrieved_songs) > 0
                and valid_recs
                and keyword_match
                and confidence > 0.5
            )

        confidence_scores.append(confidence)

        if success:
            passed += 1
            result = "PASS"
        else:
            result = "FAIL"

        print(f"\nTest {index}: {result}")
        print(f"Input: {repr(user_input)}")
        print(f"Guardrail message: {message}")
        print(f"Retrieved songs: {[song['title'] for song in retrieved_songs]}")
        print(f"Recommendations: {[song['title'] for song in recommendations]}")
        print(f"Confidence: {confidence}")

    average_confidence = round(sum(confidence_scores) / len(confidence_scores), 2)

    print("\n" + "=" * 40)
    print(f"Summary: {passed} out of {total} tests passed.")
    print(f"Average confidence score: {average_confidence}")

    if passed == total:
        print("Result: Evaluation passed.")
    else:
        print("Result: Evaluation found weaknesses that need review.")


if __name__ == "__main__":
    run_evaluation()
