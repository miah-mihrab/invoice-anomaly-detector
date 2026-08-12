-- Create role and database if they don't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anomaly_user') THEN
    CREATE ROLE anomaly_user WITH LOGIN PASSWORD 'password';
  END IF;
END $$;

ALTER ROLE anomaly_user CREATEDB;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'anomaly_db') THEN
    CREATE DATABASE anomaly_db OWNER anomaly_user;
  END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE anomaly_db TO anomaly_user;
