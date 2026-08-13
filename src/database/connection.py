import os

from sqlalchemy import create_engine


# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------

PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB")


# ---------------------------------------------------------
# Validate required environment variables
# ---------------------------------------------------------

required_variables = {
    "PG_USER": PG_USER,
    "PG_PASS": PG_PASS,
    "PG_DB": PG_DB,
}

missing_variables = [
    name
    for name, value in required_variables.items()
    if not value
]

if missing_variables:
    raise RuntimeError(
        "Missing database environment variables: "
        + ", ".join(missing_variables)
    )


# ---------------------------------------------------------
# SQLAlchemy connection URL
# ---------------------------------------------------------

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{PG_USER}:{PG_PASS}@"
    f"{PG_HOST}:{PG_PORT}/"
    f"{PG_DB}"
)


# ---------------------------------------------------------
# Database engine
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)