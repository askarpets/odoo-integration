# Odoo Integration

A sample FastAPI-based service designed to retrieve contacts and invoices info from Odoo API and store it to local PostgreSQL database.
The service exposes 4 endpoints to provide access to the retrieved resources.

## Local Deployment

### 1. Clone the repository

```bash
git clone git@github.com:askarpets/odoo-integration.git
cd odoo-integration
```

### 2. Configure environment variables

Create the necessary configuration files in the `.configs` directory:
- `.env.api` - Environment variables for the API
- `.env.postgress` - Environment variables for PostgreSQL

### 3. Build and run the services

Build the Docker images:
```bash
make build
```

Start the services:
```bash
make up
```

## API Documentation

Once the services are running, you can access the API documentation at http://localhost:8000/api/docs

We assume that there is an external auth service that provides JWT tokens, which should be attached as request headers to get access to the resources.
We use the signature public key to verify such tokens and check their expiration timestamps.  
