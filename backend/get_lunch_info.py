from scrapers import get_all_scrapers


def get_restaurants_by_region(region="kamppi"):
    all_scrapers = get_all_scrapers()
    return {name: scraper for name, scraper in all_scrapers.items() if scraper.region == region}


def get_lunch_info(restaurant_shorthand, region="kamppi", lang="fi"):
    scrapers_region = get_restaurants_by_region(region)
    scraper = scrapers_region.get(restaurant_shorthand.lower())
    if scraper:
        return scraper.get_lunch_info(lang)
    else:
        return f"No scraper found for restaurant: {restaurant_shorthand}"
