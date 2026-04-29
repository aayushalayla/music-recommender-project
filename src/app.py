import streamlit as st

try:
    from agent import run_agentic_recommender
    from specializer import STYLE_PROFILES
except ImportError:
    from src.agent import run_agentic_recommender
    from src.specializer import STYLE_PROFILES


st.title("AI Music Recommender System")

st.write(
    "This app uses multi-source retrieval, an observable agentic workflow, "
    "specialized recommendation styles, confidence scoring, and guardrails."
)

user_input = st.text_input(
    "What kind of music do you want?",
    placeholder="Example: dreamy sad songs for studying"
)

style = st.selectbox(
    "Choose recommendation style",
    list(STYLE_PROFILES.keys())
)

if st.button("Get Recommendations"):
    result = run_agentic_recommender(user_input, style=style)

    if result["status"] == "rejected":
        st.warning(result["message"])
        st.write(f"Confidence score: {result['confidence']}")

    elif result["status"] == "no_matches":
        st.warning(result["message"])
        st.write(f"Confidence score: {result['confidence']}")

    else:
        st.subheader("Recommended Songs")

        for index, rec in enumerate(result["recommendations"], start=1):
            st.markdown(f"**{index}. {rec['title']} — {rec['artist']}**")
            st.write(rec["reason"])

        st.write(f"Confidence score: {result['confidence']}")

    with st.expander("Agent Trace"):
        for step in result["trace"]:
            st.markdown(f"**{step['step']}**")
            st.write(step["action"])
            st.write(step["result"])

    with st.expander("RAG Enhancement Measurement"):
        st.write(result["rag_comparison"])

    with st.expander("Specialization Comparison"):
        st.write(result["specialization_comparison"])

    with open("logs/recommender.log", "a") as log_file:
        log_file.write(f"Input: {user_input}\n")
        log_file.write(f"Style: {style}\n")
        log_file.write(f"Result: {result}\n\n")
