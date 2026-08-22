CREATE TABLE anomaly_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,

    model_flagged_unsupervised BOOLEAN NOT NULL,
    model_flagged_supervised BOOLEAN NOT NULL,
    model_score NUMERIC(6, 4),


    reviewer_decision VARCHAR(20) NOT NULL
        CHECK (reviewer_decision IN ('confirmed_anomaly', 'false_positive')),
    reviewer_notes TEXT,

    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_anomaly_reviews_invoice_id ON anomaly_reviews(invoice_id);