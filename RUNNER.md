# Invoice Anomaly Detector — Runner Guide

This file contains the commands needed to start, stop, reset,
and resume the Invoice Anomaly Detector project.

The project uses Docker Compose for PostgreSQL and the ML environment.

---

# 1. First Time Setup

Use this when cloning the repository for the first time.

```bash
# Clone the GitHub repository.
git clone <REPOSITORY_URL>

# Move into the project directory.
cd invoice-anomaly-detector
```

Create `.env` in the project root:

```env
PG_USER=anomaly_user
PG_PASS=your_password
PG_DB=anomaly_db
PG_HOST=postgres
PG_PORT=5432
```
---

# 2. First Time Docker Setup

Use this when starting the project for the first time.

```bash
# Build the Docker images and start all services in the background.
docker compose up -d --build

# Check that all services are running.
docker compose ps

# Generate the synthetic dataset.
docker compose exec ml python -m src.data.generate

# Check the generated record counts.
docker compose exec postgres psql -U anomaly_user -d anomaly_db -c "
SELECT 'suppliers' AS table_name, COUNT(*) FROM suppliers
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'invoices', COUNT(*) FROM invoices
UNION ALL
SELECT 'invoice_items', COUNT(*) FROM invoice_items
UNION ALL
SELECT 'anomaly_labels', COUNT(*) FROM anomaly_labels;
"

# 3. Normal Resume Workflow

Use this when returning to the project after previously stopping
the containers with `docker compose down`.

```bash
# Start the existing Docker environment.
docker compose up -d

# Check that the containers are running.
docker compose ps

```

Do NOT run the data generator every time.

The PostgreSQL Docker volume preserves the existing dataset.

---

# 4. Normal Development Session

```bash
# Start the existing environment.
docker compose up -d

# Verify that the services are running.
docker compose ps

# Work on the project / notebooks / models.

# When finished, stop the containers while preserving PostgreSQL data.
docker compose down
```

---

# 5. Starting Jupyter

Jupyter is used for EDA and ML experimentation.

```bash
# Start JupyterLab inside the ML container.
docker compose exec ml jupyter lab --ip=0.0.0.0 --no-browser --allow-root
```

---

# 6. Docker Rebuild

Use this when Docker-related files or dependencies have changed.

Examples:

- `Dockerfile` changed
- `docker-compose.yml` changed
- Python dependencies changed
- System packages changed

```bash
# Rebuild the Docker images and start the services.
docker compose up -d --build

# Verify the services.
docker compose ps
```

You normally do NOT need `--build` when simply resuming work.

---

# 7. Stop the Project

```bash
# Stop the containers while keeping PostgreSQL data.
docker compose down
```

Later, resume with:

```bash
# Start the existing containers again.
docker compose up -d
```

---

# 8. Complete Database Reset

WARNING: This deletes the PostgreSQL Docker volume.

Only use this when you intentionally want a completely fresh
database and dataset.

```bash
# Stop all containers and DELETE Docker volumes.
docker compose down -v

# Rebuild the Docker environment.
docker compose up -d --build

# Generate a completely fresh synthetic dataset.
docker compose exec ml python -m src.data.generate

# Verify the generated data.
docker compose exec postgres psql -U anomaly_user -d anomaly_db -c "
SELECT 'suppliers' AS table_name, COUNT(*) FROM suppliers
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'invoices', COUNT(*) FROM invoices
UNION ALL
SELECT 'invoice_items', COUNT(*) FROM invoice_items
UNION ALL
SELECT 'anomaly_labels', COUNT(*) FROM anomaly_labels;
"
```

---

# 9. PostgreSQL

Open PostgreSQL:

```bash
# Open the PostgreSQL shell inside the container.
docker compose exec postgres psql -U anomaly_user -d anomaly_db
```

Inside PostgreSQL:

```sql
-- Show all tables.
\dt

-- Show the invoices table structure.
\d invoices

-- Show the invoice_items table structure.
\d invoice_items

-- Exit PostgreSQL.
\q
```

---

# 10. Check Data

```bash
# Count records in all main tables.
docker compose exec postgres psql -U anomaly_user -d anomaly_db -c "
SELECT 'suppliers' AS table_name, COUNT(*) FROM suppliers
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'invoices', COUNT(*) FROM invoices
UNION ALL
SELECT 'invoice_items', COUNT(*) FROM invoice_items
UNION ALL
SELECT 'anomaly_labels', COUNT(*) FROM anomaly_labels;
"

# Show the known synthetic anomaly types.
docker compose exec postgres psql -U anomaly_user -d anomaly_db -c "
SELECT anomaly_type, COUNT(*)
FROM anomaly_labels
GROUP BY anomaly_type
ORDER BY anomaly_type;
"
```

---

# 11. Synthetic Data Generation

The project uses synthetic data

Generate the dataset:

```bash
# Generate suppliers, customers, products, invoices,
# invoice items, and intentionally injected anomalies.
docker compose exec ml python -m src.data.generate
```

Do not run this unnecessarily because the generator creates
a new dataset.

After a database reset with `docker compose down -v`,
running the generator is required.

# 12. Current Project Workflow

The project is being developed in stages:

```text
Synthetic Data
      ↓
PostgreSQL
      ↓
EDA
      ↓
Feature Engineering
      ↓
Anomaly Detection
      ↓
Model Evaluation
      ↓
Model Persistence
      ↓
ML Prediction Service
      ↓
NestJS API
      ↓
React Client
```

# 13. Quick Resume

When coming back to the project, normally this is all that is needed:

```bash
# Start the existing Docker environment.
docker compose up -d

# Check that everything is running.
docker compose ps
```

Then continue from the current notebook/model development step.

---

# 14. IMPORTANT — `down` vs `down -v`

Normal:

```bash
# Stops containers but preserves PostgreSQL data.
docker compose down
```

Safe for normal development.

Destructive:

```bash
# Stops containers AND deletes PostgreSQL Docker volumes.
docker compose down -v
```

This deletes the database.

After `down -v`, you must recreate the dataset:

```bash
# Start the fresh Docker environment.
docker compose up -d --build

# Generate the synthetic dataset again.
docker compose exec ml python -m src.data.generate
```
