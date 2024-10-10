# Lunssi

Lunssi is a website displaying lunch menus near the Futurice office: lunssi.fly.dev/

## Development

## Frontend

### Starting the frontend

The backend runs locally on port 3000 using. The backend can be run with commands `npm ci` and `npm run`.

### Deploy to fly.io

Deploy frontend with `flyctl deploy`.

When deploying, set `BACKEND_API_URL=https://lunssi-backend.fly.dev` in `.env`.

Add env variables with `flyctl secrets set SECRET_NAME=secret`

## Backend

The backend of the application is built with Python and FastAPI. The backend runs at https://lunssi-backend.fly.dev/.

### Starting the backend

The backend runs locally on port 8080 using uvicorn. Starting the backend can be triggered with make.py using command `make run`.

### Creating a virtual environment

### Loading dependencies

### Deploy to fly.io

Deploy backend with `flyctl deploy`.
