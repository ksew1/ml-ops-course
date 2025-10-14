from joblib import load
import numpy as np
from sklearn.base import ClassifierMixin


def load_model(path="model/model.joblib") -> ClassifierMixin:
    return load(path)


def predict(model, features: dict) -> str:
    x = np.array(
        [
            [
                features["sepal_length"],
                features["sepal_width"],
                features["petal_length"],
                features["petal_width"],
            ]
        ]
    )
    class_idx = model.predict(x)[0]
    class_name = ["setosa", "versicolor", "virginica"][class_idx]
    return class_name
