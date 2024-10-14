# Lunssi

Lunssi is a website displaying lunch menus near the Futurice office: lunssi.fly.dev/

# Frontend

## Development & Setup

### Starting the frontend

The backend runs locally on port 3000 using. The backend can be run with commands `npm ci` and `npm run`.

### Deploy to fly.io

Deploy frontend with `flyctl deploy`.

When deploying, set `BACKEND_API_URL=https://lunssi-backend.fly.dev` in `.env`.

Add env variables with `flyctl secrets set SECRET_NAME=secret`

## Backend

The backend of the application is built with Python and FastAPI. The backend runs at https://lunssi-backend.fly.dev/.

## Development & Setup

### Creating a virtual environment

There are different options for creating virtual environments for python such as conda and venv. The instructions will be added here at some point.

### Loading dependencies

Dependencies are managed in `requirements.txt`.

Load requirements with `pip install -r requirements.txt` .

### Install git pre-commit hooks

1. Go to the root of the repository where you can see `backend` and `frontend`.

2. Install pre-commit with: `pre-commit install`.

Pre-commit hooks use `black` to format automatically files, when trying to commit them.

### Starting the backend

The backend runs locally on port 8080 using uvicorn. Starting the backend can be triggered with make.py using command `make run`.

### Deploy to fly.io

Deploy backend with `flyctl deploy`.
