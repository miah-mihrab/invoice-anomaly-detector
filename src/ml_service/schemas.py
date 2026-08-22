from pydantic import BaseModel


class InvoiceItemInput(BaseModel):
    """One line item on the invoice being scored."""
    quantity: float
    unit_price: float
    tax_rate: float


class InvoicePredictRequest(BaseModel):
    invoice_id: str
    items: list[InvoiceItemInput]


class InvoicePredictResponse(BaseModel):
    invoice_id: str
    is_anomaly_unsupervised: bool     # Isolation Forest flag
    is_anomaly_supervised: bool        # Random Forest flag
    anomaly_score: float               # Random Forest's probability, for the UI to show
    reasons: list[str]                  # human-readable, e.g. "unusual tax rate: 27%"