-- =========================================================
-- Suppliers
-- =========================================================

-- Stores companies that supply products.
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Supplier's business name.
    name VARCHAR(150) NOT NULL,

    -- Country where the supplier operates.
    country VARCHAR(100) NOT NULL,

    -- Currency normally used by the supplier.
    currency VARCHAR(3) NOT NULL DEFAULT 'GBP',

    -- Timestamp when the supplier was created.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================================
-- Customers
-- =========================================================

-- Stores companies that purchase products.
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Customer's business name.
    name VARCHAR(150) NOT NULL,

    -- Customer's country.
    country VARCHAR(100) NOT NULL,

    -- Useful for generating different purchasing behaviour.
    customer_type VARCHAR(50) NOT NULL,

    -- Timestamp when the customer was created.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================================
-- Products
-- =========================================================

-- Stores the product catalogue.
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Internal product code.
    sku VARCHAR(50) NOT NULL UNIQUE,

    -- Human-readable product name.
    name VARCHAR(150) NOT NULL,

    -- Product category.
    category VARCHAR(100) NOT NULL,

    -- Approximate underlying product cost.
    -- This is NOT necessarily the selling price.
    base_cost NUMERIC(12, 2) NOT NULL,

    -- Default unit used by the product.
    unit VARCHAR(30) NOT NULL DEFAULT 'unit',

    -- Timestamp when the product was created.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================================
-- Invoices
-- =========================================================

-- Stores invoice-level information.
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Human-readable invoice number.
    invoice_number VARCHAR(50) NOT NULL UNIQUE,

    -- Supplier who issued the invoice.
    supplier_id UUID NOT NULL REFERENCES suppliers(id),

    -- Customer who received the invoice.
    customer_id UUID NOT NULL REFERENCES customers(id),

    -- Date the invoice was issued.
    invoice_date TIMESTAMPTZ NOT NULL,

    -- Currency used for this invoice.
    currency VARCHAR(3) NOT NULL DEFAULT 'GBP',

    -- Invoice financial totals.
    subtotal NUMERIC(15, 2) NOT NULL,
    discount NUMERIC(15, 2) NOT NULL DEFAULT 0,
    tax_rate NUMERIC(5, 2) NOT NULL,
    tax_amount NUMERIC(15, 2) NOT NULL,
    total NUMERIC(15, 2) NOT NULL,

    -- Timestamp when the record entered the database.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================================
-- Invoice Items
-- =========================================================

-- Stores individual products/services contained in an invoice.
CREATE TABLE invoice_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Invoice containing this item.
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,

    -- Product being sold.
    product_id UUID NOT NULL REFERENCES products(id),

    -- Number of units sold.
    quantity NUMERIC(15, 3) NOT NULL,

    -- Unit price charged to this customer.
    unit_price NUMERIC(15, 2) NOT NULL,

    -- Item-level discount.
    discount NUMERIC(15, 2) NOT NULL DEFAULT 0,

    -- Tax rate applied to this item.
    tax_rate NUMERIC(5, 2) NOT NULL,

    -- Calculated tax amount.
    tax_amount NUMERIC(15, 2) NOT NULL,

    -- Amount before tax.
    subtotal NUMERIC(15, 2) NOT NULL,

    -- Final item total.
    total NUMERIC(15, 2) NOT NULL
);


-- =========================================================
-- Indexes
-- =========================================================

-- These indexes will make our future analytical queries faster.

CREATE INDEX idx_invoices_supplier_id
    ON invoices(supplier_id);

CREATE INDEX idx_invoices_customer_id
    ON invoices(customer_id);

CREATE INDEX idx_invoices_invoice_date
    ON invoices(invoice_date);

CREATE INDEX idx_invoice_items_invoice_id
    ON invoice_items(invoice_id);

CREATE INDEX idx_invoice_items_product_id
    ON invoice_items(product_id);