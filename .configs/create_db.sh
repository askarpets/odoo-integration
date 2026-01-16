#!/bin/bash
set -e

# Check if required environment variables are set
required_vars=("POSTGRES_USER" "DB_NAME")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

# Create databases and grant privileges
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL || { echo "Database creation failed"; exit 1; }
	CREATE DATABASE "${DB_NAME}";
	GRANT ALL PRIVILEGES ON DATABASE "${DB_NAME}" TO "${POSTGRES_USER}";
EOSQL

echo "Database created successfully"
