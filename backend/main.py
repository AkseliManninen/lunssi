import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from get_lunch_info import get_lunch_info
from typing import Optional

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Remove caching globally to prevent receiving old menus.
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/")
async def hello_fly():
    return "Lunssin bäkkäri"


@app.get("/restaurant")
async def get_restaurant(name: Optional[str], lang: Optional[str] = "fi"):
    try:
        res = get_lunch_info(name, lang)
        full_name, menu, lunch_price, lunch_available = res
    except Exception as e:
        logging.error(f"Error getting lunch info for {name}: {e}")
        menu, lunch_price, lunch_available = f"Error {name}: {e}", 0, 0
    return {
        "name": full_name,
        "lunchItems": menu,
        "lunchPrice": lunch_price,
        "lunchTime": lunch_available,
    }
