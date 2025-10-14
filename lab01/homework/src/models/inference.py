from pathlib import Path
from joblib import load as joblib_load
from sentence_transformers import SentenceTransformer

MODEL_DIR = Path("model")

sentence_model = SentenceTransformer(str(MODEL_DIR / "sentence-transformer"))
classifier = joblib_load(MODEL_DIR / "logistic-regression.joblib")

CLASS_LABELS = {0: "negative", 1: "neutral", 2: "positive"}


def predict_sentiment(text: str) -> str:
    embedding = sentence_model.encode(text, convert_to_numpy=True)
    class_id = classifier.predict([embedding])[0]
    return CLASS_LABELS.get(class_id, "unknown")
