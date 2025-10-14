from fastapi.testclient import TestClient
from src.app import app
from src.models.inference import sentence_model, classifier, predict_sentiment
import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression

client = TestClient(app)


@pytest.mark.parametrize(
    "invalid_payload, error_field",
    [
        ({}, "text"),  # Missing key
        ({"text": ""}, "text"),  # Empty string
        ({"text": None}, "text"),  # Null input
        ({"txt": "value"}, "text"),  # Wrong key
        ({"text": 123}, "text"),  # Wrong type
    ],
)
def test_invalid_input_returns_422(invalid_payload, error_field):
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()

    assert isinstance(data, dict)
    assert "detail" in data

    error_fields = [
        e["loc"][-1]
        for e in data["detail"]
        if e["type"].startswith("value_error") or e["loc"][-1] == error_field
    ]
    assert error_field in error_fields


def test_model_loading_success():
    assert sentence_model is not None
    assert classifier is not None
    assert isinstance(classifier, LogisticRegression)
    assert hasattr(sentence_model, "encode")


def test_embedding_and_prediction_shape():
    text = "Test sentence for embedding"
    embedding = sentence_model.encode(text, convert_to_numpy=True)

    assert isinstance(embedding, np.ndarray)
    assert embedding.ndim == 1  # Should be a 1D vector
    assert embedding.shape[0] > 0  # Number of features

    prediction = classifier.predict([embedding])[0]
    assert prediction in [0, 1, 2]


@pytest.mark.parametrize(
    "input_text, expected_labels",
    [
        ("The movie was amazing", ["positive"]),
        ("Does what it supposed to do", ["neutral"]),
        ("Terrible service, would not recommend", ["negative"]),
    ],
)
def test_predict_output_valid(input_text, expected_labels):
    response = client.post("/predict", json={"text": input_text})
    assert response.status_code == 200

    json_data = response.json()

    assert isinstance(json_data, dict)
    assert "prediction" in json_data
    assert type(json_data["prediction"]) is str
    assert json_data["prediction"] in ["positive", "neutral", "negative"]
    assert json_data["prediction"] in expected_labels


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Absolutely loved it!", "positive"),
        ("Does what it supposed to do", "neutral"),
        ("Worst experience ever", "negative"),
    ],
)
def test_predict_sentiment_direct(text, expected):
    result = predict_sentiment(text)
    assert isinstance(result, str)
    assert result in ["positive", "neutral", "negative"]
    assert result == expected
