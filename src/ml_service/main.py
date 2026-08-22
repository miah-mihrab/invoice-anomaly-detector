from fastapi import FastAPI

from .model_loader import model_bundle
from .features import build_invoice_features, explain_flags
from .schemas import InvoicePredictRequest, InvoicePredictResponse

app = FastAPI(title="Invoice Anomaly Detector - ML Service")


@app.get("/health")
def health():
    # Simple liveness check for NestJS / Docker healthchecks to poll.
    return {"status": "ok"}


@app.post("/predict", response_model=InvoicePredictResponse)
def predict(request: InvoicePredictRequest):
    X = build_invoice_features(request.items)

    # Isolation Forest: -1 means flagged as anomaly, 1 means normal.
    iso_flagged = model_bundle.isolation_forest.predict(X)[0] == -1

    # Random Forest: predict() gives the flag, predict_proba() gives a
    # confidence score — more useful for the UI than a bare True/False.
    rf_flagged = bool(model_bundle.random_forest.predict(X)[0])
    rf_score = float(model_bundle.random_forest.predict_proba(X)[0][1])

    return InvoicePredictResponse(
        invoice_id=request.invoice_id,
        is_anomaly_unsupervised=bool(iso_flagged),
        is_anomaly_supervised=rf_flagged,
        anomaly_score=rf_score,
        reasons=explain_flags(X),
    )