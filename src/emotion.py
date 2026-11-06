from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def analyze_emotion(text):
    results = emotion_classifier(text)[0]

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    top = results[0]

    return {
        "emotion": top["label"],
        "confidence": top["score"],
        "all_emotions": results
    }
