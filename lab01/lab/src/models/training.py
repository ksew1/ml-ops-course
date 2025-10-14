from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import os


def load_data():
    data = load_iris()
    return data.data, data.target


def train_model():
    X, y = load_data()
    model = RandomForestClassifier()
    model.fit(X, y)
    return model


def save_model(model, path="model/model.joblib"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    dump(model, path)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    model = train_model()
    save_model(model)
