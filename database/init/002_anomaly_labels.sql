-- ---------------------------------------------------------
-- Ground-truth anomaly labels
-- ---------------------------------------------------------
-- This table records anomalies that WE intentionally create.
--
-- The ML model must NEVER use this table during training.
-- It exists only so we can compare:
--
--     Actual anomaly  vs  Model prediction
--
-- later.
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS anomaly_labels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Invoice containing the anomaly.
    invoice_id UUID NOT NULL,

    -- Human-readable invoice number.
    invoice_number VARCHAR(50) NOT NULL,

    -- Type of anomaly intentionally introduced.
    anomaly_type VARCHAR(50) NOT NULL,

    -- Always TRUE for records in this table.
    is_anomaly BOOLEAN NOT NULL DEFAULT TRUE,

    -- When the label was created.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Prevent duplicate labels for the same invoice/type.
    CONSTRAINT uq_anomaly_invoice_type
        UNIQUE (invoice_id, anomaly_type)
);