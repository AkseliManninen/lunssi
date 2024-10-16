import logging
import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from get_lunch_info import get_lunch_info
from typing import Optional

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

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


def structure_response(result, name=""):
    if isinstance(result, tuple):
        full_name, menu, lunch_price, lunch_available = result
    else:
        logging.error(f"Error getting lunch info for {name}: {result}")
        full_name = name if name else "Restaurant not found"
        menu = [f"Error: {result}"]
        lunch_price = "N/A"
        lunch_available = "N/A"

    return {
        "name": full_name,
        "lunchItems": menu,
        "lunchPrice": lunch_price,
        "lunchTime": lunch_available,
    }


@app.get("/restaurant")
async def get_restaurant(name: Optional[str], lang: Optional[str] = "fi"):
    try:
        result = await get_lunch_info(name, lang)
    except Exception as e:
        logging.error(f"Error getting lunch info for {name}: {e}")
        result = f"Error: {str(e)}"
    return structure_response(result, name)


@app.get("/restaurants")
async def get_restaurants(lang: Optional[str] = "fi"):
    restaurant_shorthands = [
        "bruuveri",
        "kansis",
        "plaza",
        "pompier_albertinkatu",
        "hämis",
        "queem",
    ]

    async def fetch_menu(restaurant):
        try:
            return await get_lunch_info(restaurant, lang)
        except Exception as e:
            logging.error(f"Error fetching lunch info for {restaurant}: {e}")
            return f"Error fetching {restaurant} menu: {str(e)}"

    # Use asyncio.gather to run all the fetches in parallel
    results = await asyncio.gather(*[fetch_menu(name) for name in restaurant_shorthands])
    response = [structure_response(res, name) for res, name in zip(results, restaurant_shorthands)]
    return response
