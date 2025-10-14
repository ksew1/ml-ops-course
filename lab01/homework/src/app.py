from fastapi import FastAPI
from src.api.models.sentiment import PredictRequest, PredictResponse
from src.models.inference import predict_sentiment

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0.0",
    description="Minimal API for predicting sentiment on a single text input",
)


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest) -> PredictResponse:
    prediction = predict_sentiment(request.text)
    return PredictResponse(prediction=prediction)
