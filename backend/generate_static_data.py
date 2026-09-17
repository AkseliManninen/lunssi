"""Scrapes every restaurant once and writes the results to static JSON files
that the frontend reads at build time. Replaces the always-on FastAPI backend
for the static-hosting setup.
"""

import asyncio
import json
import logging
from pathlib import Path

from get_lunch_info import get_lunch_info
from get_lunch_info import get_restaurants_by_region
from utils.constants import LANGUAGES
from utils.constants import REGIONS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "frontend" / "data"


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
        logging.error(f"Error getting lunch info for {requested_name}: {result}")
        discount = None
        is_student_cantine = False
        location = "N/A"
        lunch_hours = "N/A"
        lunch_price = "N/A"
        menu = [f"Error: {result}"]
        name = requested_name if requested_name else "Restaurant not found"
        url = None

    return {
        "discount": discount,
        "isStudentCantine": is_student_cantine,
        "location": location,
        "lunchHours": lunch_hours,
        "lunchPrice": lunch_price,
        "menu": menu,
        "name": name,
        "url": url,
    }


async def get_restaurants_for_region(region, lang):
    available_restaurants = get_restaurants_by_region(region)
    restaurant_shorthands = list(available_restaurants.keys())

    async def fetch_menu(restaurant):
        try:
            return await get_lunch_info(restaurant, region, lang)
        except Exception as e:
            logging.error(f"Error fetching lunch info for {restaurant}: {e}")
            return f"Error fetching {restaurant} menu: {str(e)}"

    results = await asyncio.gather(*[fetch_menu(name) for name in restaurant_shorthands])
    return [structure_response(res, name) for res, name in zip(results, restaurant_shorthands)]


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for region in REGIONS:
        for lang in LANGUAGES:
            logging.info(f"Scraping region={region} lang={lang}")
            restaurants = await get_restaurants_for_region(region, lang)
            out_path = OUTPUT_DIR / f"{region}-{lang}.json"
            out_path.write_text(json.dumps(restaurants, ensure_ascii=False, indent=2))
            logging.info(f"Wrote {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
