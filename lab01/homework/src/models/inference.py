def predict_sentiment(text: str) -> str:
    if "great" in text.lower() or "satisfied" in text.lower():
        return "positive"
    elif "terrible" in text.lower() or "bad" in text.lower():
        return "negative"
    else:
        return "neutral"
