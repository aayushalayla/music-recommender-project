import streamlit as st
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


def generate_recommendations(user_input, retrieved_songs):
    recommendations = []

    for song in retrieved_songs:
        recommendations.append({
            "title": song["title"],
            "artist": song["artist"],
            "reason": (
                f"This matches your request because it connects to "
                f"{song['mood']} moods and works for {song['activity']}."
            )
        })

    return recommendations


st.title("AI Music Recommender System")
st.write(
    "Enter a mood, activity, genre, or listening situation. "
    "The system retrieves matching songs before generating recommendations."
)

user_input = st.text_input(
    "What kind of music do you want?",
    placeholder="Example: dreamy sad songs for studying"
)

if st.button("Get Recommendations"):
    valid, message = validate_user_input(user_input)

    if not valid:
        st.warning(message)
        st.write("Confidence score: 0.20")
    else:
        retrieved_songs = retrieve_songs(user_input)
        recommendations = generate_recommendations(user_input, retrieved_songs)
        confidence = calculate_confidence(user_input, retrieved_songs)

        if not retrieved_songs:
            st.warning("No strong matches found. Try a different mood, genre, or activity.")
            st.write(f"Confidence score: {confidence}")
        elif not validate_recommendations(recommendations, retrieved_songs):
            st.error("Recommendation validation failed.")
        else:
            st.subheader("Recommended Songs")

            for index, rec in enumerate(recommendations, start=1):
                st.markdown(f"**{index}. {rec['title']} — {rec['artist']}**")
                st.write(rec["reason"])

            st.write(f"Confidence score: {confidence}")

            with open("logs/recommender.log", "a") as log_file:
                log_file.write(f"Input: {user_input}\n")
                log_file.write(f"Retrieved: {retrieved_songs}\n")
                log_file.write(f"Recommendations: {recommendations}\n")
                log_file.write(f"Confidence: {confidence}\n\n")
