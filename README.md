# Lunssi

Lunssi is a website displaying lunch menus near the Futurice office: https://lunssi.fly.dev.

## Installation

- Install [Task](https://taskfile.dev/installation/)
- Initialize project with `task init`. This command installs all necessary
  dependencies for both the frontend and backend. It also creates a Python
  virtual environment for the backend to manage its dependencies.

## Frontend

The frontend is built with Next.js.

### Starting the frontend

Start a development server with `task dev:frontend`. The server runs on port 3000.

### Deploy to fly.io

Deploy the frontend with `flyctl deploy`.

When deploying, set `BACKEND_API_URL=https://lunssi-backend.fly.dev` in `.env`.

Add env variables with `flyctl secrets set SECRET_NAME=secret`

### Backend

The backend of the application is built with Python and FastAPI. The backend
runs at https://lunssi-backend.fly.dev/.

### Starting the backend

Start the backend with `task dev:backend`. This command activates the Python
virtual environment and starts the backend with hot-reloading enabled. The
backend will run locally on port 8080 using uvicorn.

### Deploy to fly.io

Deploy the backend with `flyctl deploy`.
