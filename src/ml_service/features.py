import numpy as np
import pandas as pd

from .model_loader import model_bundle
from .schemas import InvoiceItemInput


def build_invoice_features(items: list[InvoiceItemInput]) -> pd.DataFrame:
    """Rebuilds the exact same 6 features used in training, for ONE
    invoice's items. Uses the frozen median/MAD/valid-rates from
    feature_stats.json instead of recalculating them"""

    stats = model_bundle.feature_stats

    df = pd.DataFrame([item.model_dump() for item in items])
    
    df["quantity_zscore"] = (
        (df["quantity"] - stats["quantity_median"])
        / (1.4826 * stats["quantity_mad"])
    )
    df["unit_price_zscore"] = (
        (df["unit_price"] - stats["unit_price_median"])
        / (1.4826 * stats["unit_price_mad"])
    )

    # --- invalid tax rate flag, using the FROZEN list of common rates ---
    valid_rates = set(stats["valid_tax_rates"])
    df["invalid_tax_rate"] = ~df["tax_rate"].isin(valid_rates)

    threshold = stats["zscore_outlier_threshold"]

    # --- aggregate item-level -> single-row invoice-level features,
    # same aggregation logic as the notebook's groupby().agg() ---
    features = {
        "item_count": len(df),
        "max_quantity_zscore": df["quantity_zscore"].max(),
        "max_unit_price_zscore": df["unit_price_zscore"].max(),
        "num_quantity_outliers": int((df["quantity_zscore"] > threshold).sum()),
        "num_price_outliers": int((df["unit_price_zscore"] > threshold).sum()),
        "num_invalid_tax_rate": int(df["invalid_tax_rate"].sum()),
    }

    return pd.DataFrame([features])[stats["feature_cols"]]


def explain_flags(feature_row: pd.DataFrame) -> list[str]:
    row = feature_row.iloc[0]
    reasons = []

    if row["num_quantity_outliers"] > 0:
        reasons.append(f"Unusual quantity on {int(row['num_quantity_outliers'])} item(s)")
    if row["num_price_outliers"] > 0:
        reasons.append(f"Unusual unit price on {int(row['num_price_outliers'])} item(s)")
    if row["num_invalid_tax_rate"] > 0:
        reasons.append(f"Uncommon tax rate on {int(row['num_invalid_tax_rate'])} item(s)")

    return reasons