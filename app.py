import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from src.speech_to_text import recognize_speech
from src.sentiment import analyze_sentiment
from src.emotion import analyze_emotion


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="SentiVoice",
    page_icon="🎤",
    layout="wide"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🎤 SentiVoice")

st.subheader(
    "Speech-Based Sentiment & Emotion Analyzer"
)

st.write(
    "Speak into your microphone and let AI analyze "
    "the sentiment and emotion of your speech."
)


# -----------------------------
# SESSION STATE
# -----------------------------

if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("⚙️ Settings")

st.sidebar.write(
    "SentiVoice uses speech recognition, "
    "sentiment analysis and an emotion classification model."
)


# -----------------------------
# RECORD BUTTON
# -----------------------------

st.header("🎙️ Speech Input")

if st.button("🎤 Start Recording", use_container_width=True):

    with st.spinner("Listening..."):

        text = recognize_speech()

    st.session_state.current_text = text


# -----------------------------
# TEXT INPUT
# -----------------------------

st.header("📝 Transcribed Speech")

text = st.text_area(
    "You can also type text manually for testing:",
    value=st.session_state.get("current_text", ""),
    height=120
)


# -----------------------------
# ANALYZE
# -----------------------------

if st.button(
    "🧠 Analyze Emotion",
    use_container_width=True
):

    if not text.strip():

        st.warning("Please speak or enter some text.")

    else:

        with st.spinner("Analyzing..."):

            sentiment_result = analyze_sentiment(text)

            emotion_result = analyze_emotion(text)


        # -------------------------
        # DISPLAY RESULTS
        # -------------------------

        st.header("📊 Analysis Result")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Sentiment",
                sentiment_result["sentiment"]
            )


        with col2:

            st.metric(
                "Emotion",
                emotion_result["emotion"].upper()
            )


        with col3:

            st.metric(
                "Confidence",
                f"{emotion_result['confidence'] * 100:.2f}%"
            )


        st.divider()


        # -------------------------
        # SENTIMENT SCORES
        # -------------------------

        st.subheader("📈 Sentiment Scores")


        sentiment_data = pd.DataFrame(
            {
                "Sentiment": [
                    "Positive",
                    "Neutral",
                    "Negative"
                ],

                "Score": [
                    sentiment_result["positive"],
                    sentiment_result["neutral"],
                    sentiment_result["negative"]
                ]
            }
        )


        st.bar_chart(
            sentiment_data.set_index("Sentiment")
        )


        # -------------------------
        # EMOTION SCORES
        # -------------------------

        st.subheader("😊 Emotion Distribution")


        emotion_data = pd.DataFrame(
            emotion_result["all_emotions"]
        )

        emotion_data["score"] = (
            emotion_data["score"] * 100
        )


        st.bar_chart(
            emotion_data.set_index("label")
        )


        # -------------------------
        # SAVE HISTORY
        # -------------------------

        record = {

            "Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "Text": text,

            "Sentiment":
                sentiment_result["sentiment"],

            "Emotion":
                emotion_result["emotion"],

            "Confidence":
                emotion_result["confidence"]

        }


        st.session_state.history.append(record)


# -----------------------------
# HISTORY
# -----------------------------

st.divider()

st.header("📜 Analysis History")


if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No analysis performed yet."
    )