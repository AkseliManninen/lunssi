import logging
import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from get_lunch_info import get_lunch_info
from get_lunch_info import get_restaurants_by_region
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


def structure_response(result, requested_name):
    if isinstance(result, tuple):
        (
            discount,
            is_student_cantine,
            location,
            lunch_hours,
            lunch_price,
            menu,
            name,
            url,
        ) = result
    else:
        logging.error(f"Error getting lunch info for {name}: {result}")
        location = "N/A"
        lunch_hours = "N/A"
        lunch_price = "N/A"
        menu = [f"Error: {result}"]
        name = requested_name if requested_name else "Restaurant not found"

    return {
        "discount": discount,
        "isStudentCantine": is_student_cantine,
        "location": location,
        "lunchHours": lunch_hours,
        "lunchPrice": lunch_price,
        "menu": menu,
        "name": name,
    }


@app.get("/restaurant")
async def get_restaurant(name: Optional[str], region: Optional[str], lang: Optional[str] = "fi"):
    try:
        result = await get_lunch_info(name, region, lang)
    except Exception as e:
        logging.error(f"Error getting lunch info for {name}: {e}")
        result = f"Error: {str(e)}"
    return structure_response(result, name)


@app.get("/restaurants")
async def get_restaurants(region: Optional[str] = "kamppi", lang: Optional[str] = "fi"):
    available_restaurants = get_restaurants_by_region(region)
    restaurant_shorthands = list(available_restaurants.keys())

    async def fetch_menu(restaurant):
        try:
            return await get_lunch_info(restaurant, region, lang)
        except Exception as e:
            logging.error(f"Error fetching lunch info for {restaurant}: {e}")
            return f"Error fetching {restaurant} menu: {str(e)}"

    # Use asyncio.gather to run all the fetches in parallel
    results = await asyncio.gather(*[fetch_menu(name) for name in restaurant_shorthands])
    response = [structure_response(res, name) for res, name in zip(results, restaurant_shorthands)]
    return response
