import json
import joblib
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parents[2] / "models"


class ModelBundle:
    def __init__(self):
        self.isolation_forest = joblib.load(MODELS_DIR / "isolation_forest.pkl")
        self.random_forest = joblib.load(MODELS_DIR / "random_forest.pkl")

        with open(MODELS_DIR / "feature_stats.json") as f:
            self.feature_stats = json.load(f)


# A single shared instance, imported by main.py and features.py.
model_bundle = ModelBundle()