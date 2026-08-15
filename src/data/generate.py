import os
import random
import uuid
from decimal import Decimal
import psycopg
from faker import Faker


fake = Faker("en-GB")


random.seed(42)
Faker.seed(42)



# ---------------------------------------------------------
# PostgreSQL configuration
# ---------------------------------------------------------

# Read PostgreSQL connection settings from environment variables.
DATABASE_CONFIG = {
    "host": os.getenv("PG_HOST", "postgres"),
    "port": int(os.getenv("PG_PORT", "5432")),
    "dbname": os.getenv("PG_DB", "anomaly_db"),
    "user": os.getenv("PG_USER", "anomaly_user"),
    "password": os.getenv("PG_PASS", "anomaly_password"),
}

SUPPLIER_COUNT = 100
CUSTOMER_COUNT = 500
PRODUCT_COUNT = 5000


INVOICE_COUNT = 10_000
MIN_ITEMS_PER_INVOICE = 1
MAX_ITEMS_PER_INVOICE = 30
ANOMALY_RATE = 0.02


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)



def generate_suppliers(connection):
    """Generate synthetic suppliers."""

    suppliers = []

    for _ in range(SUPPLIER_COUNT):
        supplier_id = uuid.uuid4()

        name = fake.company()

        country = random.choice([
            "United Kingdom",
            "Ireland",
            "France",
            "Germany",
            "Netherlands",
        ])

        currency = "GBP"

        suppliers.append({
            "id": supplier_id,
            "name": name,
            "country": country,
            "currency": currency,
        })



    with connection.cursor() as cursor:
        for supplier in suppliers:
            cursor.execute(
                """
                INSERT INTO suppliers(
                    id,
                    name,
                    country,
                    currency
                )
                VALUES(%s, %s, %s, %s)
                """,
                 (
                    supplier["id"],
                    supplier["name"],
                    supplier["country"],
                    supplier["currency"],
                )
            )

    connection.commit()

    print(f"Generated {len(suppliers)} suppliers.")

    return suppliers    



def generate_customers(connection):

    customers = []

    for _ in range(CUSTOMER_COUNT):

        customer_id = uuid.uuid4()

        name = fake.company()

        country = random.choice([
            "United Kingdom",
            "Ireland",
        ])

        customer_type = random.choice([
            "restaurant",
            "hotel",
            "retailer",
            "wholesaler",
            "cafe",
        ])

        customers.append({
            "id": customer_id,
            "name": name,
            "country": country,
            "customer_type": customer_type,
        })

    with connection.cursor() as cursor:

        for customer in customers:

            cursor.execute(
                """
                INSERT INTO customers (
                    id,
                    name,
                    country,
                    customer_type
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    customer["id"],
                    customer["name"],
                    customer["country"],
                    customer["customer_type"],
                ),
            )

    connection.commit()

    print(f"Generated {len(customers)} customers.")

    return customers


PRODUCT_CATEGORIES = {
    "Dairy": [
        "Whole Milk 1L",
        "Semi Skimmed Milk 1L",
        "Butter 250g",
        "Cheddar Cheese 500g",
        "Greek Yogurt 500g",
    ],
    "Bakery": [
        "White Bread",
        "Wholemeal Bread",
        "Croissant",
        "Baguette",
        "Burger Bun",
    ],
    "Beverages": [
        "Orange Juice 1L",
        "Apple Juice 1L",
        "Mineral Water 500ml",
        "Cola 500ml",
        "Sparkling Water 750ml",
    ],
    "Produce": [
        "Tomatoes 1kg",
        "Potatoes 2kg",
        "Onions 1kg",
        "Apples 1kg",
        "Bananas 1kg",
    ],
}


def generate_products(connection):

    products = []

    product_templates = []

    for category, names in PRODUCT_CATEGORIES.items():

        for name in names:

            product_templates.append({
                "name": name,
                "category": category,
            })

    for index in range(PRODUCT_COUNT):

        template = random.choice(product_templates)

        product_id = uuid.uuid4()

        sku = f"SKU-{index + 1:05d}"

        name = template["name"]

        category = template["category"]

        # Base cost represents the approximate underlying
        # cost of the product. It is NOT the customer's price.
        base_cost = Decimal(
            str(round(random.uniform(0.50, 50.00), 2))
        )

        unit = random.choice([
            "kg",
            "each",
            "case",
        ])

        products.append({
            "id": product_id,
            "sku": sku,
            "name": name,
            "category": category,
            "base_cost": base_cost,
            "unit": unit,
        })

    with connection.cursor() as cursor:

        for product in products:

            cursor.execute(
                """
                INSERT INTO products (
                    id,
                    sku,
                    name,
                    category,
                    base_cost,
                    unit
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    product["id"],
                    product["sku"],
                    product["name"],
                    product["category"],
                    product["base_cost"],
                    product["unit"],
                ),
            )

    connection.commit()

    print(f"Generated {len(products)} products.")

    return products



def generate_customer_price(product, supplier, customer):

    base_cost = float(product["base_cost"])

    supplier_markup = random.uniform(1.15, 1.60)

    base_price = base_cost * supplier_markup

    customer_discount = random.uniform(0.90, 1.10)

    price = base_price * customer_discount

    return round(price, 2)


TAX_RATES = [
    0,
    5,
    20,
]


def generate_tax_rate():
    # Most products will use the standard rate.
    return random.choices(
        TAX_RATES,
        weights=[10, 10, 80],
        k=1,
    )[0]



def generate_quantity(product):

    unit = product["unit"]

    if unit == "kg":
        return round(random.uniform(1, 50), 3)

    if unit == "case":
        return random.randint(1, 20)

    if unit == "each":
        return random.randint(1, 30)

    return random.randint(1, 50)


# ---------------------------------------------------------
# Invoice date generation
# ---------------------------------------------------------

from datetime import datetime, timedelta, timezone


def generate_invoice_date():

    end_date = datetime.now(timezone.utc)

    days_back = random.randint(0, 365)

    return end_date - timedelta(days=days_back)



# ---------------------------------------------------------
# Invoice generation
# ---------------------------------------------------------

ANOMALY_COUNT = int(
    INVOICE_COUNT * ANOMALY_RATE
)

anomaly_invoice_numbers = set(
    random.sample(
        range(1, INVOICE_COUNT + 1),
        ANOMALY_COUNT,
    )
)


def generate_invoices(connection, suppliers, customers, products):
    """
    Generate invoices and their corresponding invoice items.

    Returns metadata about intentionally injected anomalies
    so we can evaluate our ML models later.
    """

    anomaly_records = []

    with connection.cursor() as cursor:

        for invoice_number in range(1, INVOICE_COUNT + 1):

            # -------------------------------------------------
            # Select invoice participants
            # -------------------------------------------------

            supplier = random.choice(suppliers)

            customer = random.choice(customers)

            invoice_id = uuid.uuid4()

            invoice_date = generate_invoice_date()

            # -------------------------------------------------
            # Select products
            # -------------------------------------------------

            item_count = random.randint(
                MIN_ITEMS_PER_INVOICE,
                MAX_ITEMS_PER_INVOICE,
            )

            selected_products = random.sample(
                products,
                min(item_count, len(products)),
            )

            invoice_items = []

            subtotal = Decimal("0.00")

            # -------------------------------------------------
            # Generate invoice items
            # -------------------------------------------------

            for product in selected_products:

                quantity = generate_quantity(product)

                unit_price = generate_customer_price(
                    product,
                    supplier,
                    customer,
                )

                tax_rate = generate_tax_rate()

                discount = Decimal("0.00")

                # -------------------------------------------------
                # Calculate item financial values
                # -------------------------------------------------

                item_subtotal = (
                    Decimal(str(quantity))
                    * Decimal(str(unit_price))
                )

                item_subtotal -= discount

                item_tax = (
                    item_subtotal
                    * Decimal(str(tax_rate))
                    / Decimal("100")
                )

                item_total = item_subtotal + item_tax

                subtotal += item_subtotal

                invoice_items.append({
                    "id": uuid.uuid4(),
                    "product_id": product["id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": discount,
                    "tax_rate": tax_rate,
                    "tax_amount": item_tax,
                    "subtotal": item_subtotal,
                    "total": item_total,
                })

            # -------------------------------------------------
            # Invoice-level discount
            # -------------------------------------------------

            invoice_discount = Decimal("0.00")

            if random.random() < 0.20:
                invoice_discount = (
                    subtotal
                    * Decimal(str(random.uniform(0.02, 0.10)))
                ).quantize(Decimal("0.01"))

            taxable_subtotal = subtotal - invoice_discount

            # -------------------------------------------------
            # Determine anomaly status for this invoice
            # -------------------------------------------------

            is_anomaly = (
                invoice_number in anomaly_invoice_numbers
            )

            anomaly_type = None

            # -------------------------------------------------
            # Inject occasional anomaly
            # -------------------------------------------------

            if is_anomaly and invoice_items:

                anomaly_item = random.choice(invoice_items)

                anomaly_type = random.choice([
                    "price_spike",
                    "quantity_spike",
                    "tax_error",
                ])

                # -----------------------------------------------------
                # Price anomaly
                # -----------------------------------------------------

                if anomaly_type == "price_spike":

                    # Increase the unit price substantially.
                    anomaly_item["unit_price"] = round(
                        anomaly_item["unit_price"]
                        * random.uniform(2.0, 4.0),
                        2,
                    )

                # -----------------------------------------------------
                # Quantity anomaly
                # -----------------------------------------------------

                elif anomaly_type == "quantity_spike":

                    # Increase the quantity substantially.
                    anomaly_item["quantity"] = (
                        anomaly_item["quantity"]
                        * random.randint(5, 10)
                    )

                # -----------------------------------------------------
                # Tax anomaly
                # -----------------------------------------------------

                elif anomaly_type == "tax_error":

                    # Use an unusual synthetic tax rate.
                    anomaly_item["tax_rate"] = random.choice([
                        13,
                        17,
                        27,
                    ])

                # -----------------------------------------------------
                # Recalculate the affected item
                # -----------------------------------------------------

                item_quantity = Decimal(
                    str(anomaly_item["quantity"])
                )

                item_unit_price = Decimal(
                    str(anomaly_item["unit_price"])
                )

                item_discount = Decimal(
                    str(anomaly_item["discount"])
                )

                item_tax_rate = Decimal(
                    str(anomaly_item["tax_rate"])
                )

                anomaly_item["subtotal"] = (
                    item_quantity * item_unit_price
                    - item_discount
                ).quantize(Decimal("0.01"))

                anomaly_item["tax_amount"] = (
                    anomaly_item["subtotal"]
                    * item_tax_rate
                    / Decimal("100")
                ).quantize(Decimal("0.01"))

                anomaly_item["total"] = (
                    anomaly_item["subtotal"]
                    + anomaly_item["tax_amount"]
                ).quantize(Decimal("0.01"))

            # -------------------------------------------------
            # Recalculate invoice-level totals from the
            # (possibly anomaly-adjusted) invoice items.
            # -------------------------------------------------

            subtotal = sum(
                (
                    Decimal(str(item["subtotal"]))
                    for item in invoice_items
                ),
                Decimal("0.00"),
            )

            taxable_subtotal = subtotal - invoice_discount

            invoice_tax = sum(
                (
                    Decimal(str(item["tax_amount"]))
                    for item in invoice_items
                ),
                Decimal("0.00"),
            )

            invoice_tax = invoice_tax.quantize(
                Decimal("0.01")
            )

            invoice_total = (
                taxable_subtotal + invoice_tax
            ).quantize(Decimal("0.01"))

            if taxable_subtotal > Decimal("0.00"):
                invoice_tax_rate = (
                    invoice_tax / taxable_subtotal * Decimal("100")
                ).quantize(Decimal("0.01"))
            else:
                invoice_tax_rate = Decimal("0.00")

            # -------------------------------------------------
            # Insert invoice
            # -------------------------------------------------

            invoice_number_value = (
                f"INV-{invoice_number:06d}"
            )

            cursor.execute(
                """
                INSERT INTO invoices (
                    id,
                    invoice_number,
                    supplier_id,
                    customer_id,
                    invoice_date,
                    currency,
                    subtotal,
                    discount,
                    tax_rate,
                    tax_amount,
                    total
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    invoice_id,
                    invoice_number_value,
                    supplier["id"],
                    customer["id"],
                    invoice_date,
                    "GBP",
                    subtotal,
                    invoice_discount,
                    invoice_tax_rate,
                    invoice_tax,
                    invoice_total,
                ),
            )

            if is_anomaly:

                cursor.execute(
                    """
                    INSERT INTO anomaly_labels (
                        invoice_id,
                        invoice_number,
                        anomaly_type,
                        is_anomaly
                    )
                    VALUES (%s, %s, %s, TRUE)
                    ON CONFLICT (invoice_id, anomaly_type)
                    DO NOTHING
                    """,
                    (
                        invoice_id,
                        invoice_number_value,
                        anomaly_type,
                    ),
                )

                anomaly_records.append({
                    "invoice_id": invoice_id,
                    "invoice_number": invoice_number_value,
                    "anomaly_type": anomaly_type,
                })

            # -------------------------------------------------
            # Insert invoice items
            # -------------------------------------------------

            for item in invoice_items:

                cursor.execute(
                    """
                    INSERT INTO invoice_items (
                        id,
                        invoice_id,
                        product_id,
                        quantity,
                        unit_price,
                        discount,
                        tax_rate,
                        tax_amount,
                        subtotal,
                        total
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        item["id"],
                        invoice_id,
                        item["product_id"],
                        item["quantity"],
                        item["unit_price"],
                        item["discount"],
                        item["tax_rate"],
                        item["tax_amount"],
                        item["subtotal"],
                        item["total"],
                    ),
                )

        connection.commit()

    print(f"Generated {INVOICE_COUNT} invoices.")

    print(
        f"Injected {len(anomaly_records)} known anomalies."
    )

    return anomaly_records




def main():
    """
    Generate the complete synthetic dataset.

    Generation order matters because invoices depend on
    suppliers, customers, and products already existing.
    """

    print("Connecting to PostgreSQL...")

    with get_connection() as connection:

        # Generate suppliers first.
        print("Generating suppliers...")
        suppliers = generate_suppliers(connection)

        # Generate customers.
        print("Generating customers...")
        customers = generate_customers(connection)

        # Generate products.
        print("Generating products...")
        products = generate_products(connection)

        # Generate invoices and invoice items using the
        # suppliers, customers and products above.
        print("Generating invoices...")
        generate_invoices(
            connection,
            suppliers,
            customers,
            products,
        )

    print("Synthetic dataset generation completed.")


if __name__ == "__main__":
    main()