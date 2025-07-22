from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base import RestaurantScraper


class PompierAlbertinkatuScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Pompier Albertinkatu",
            "https://pompier.fi/albertinkatu/albertinkatu-menu/",
            "14 - 19€",
            "10:45 - 14:00",
        )

    def parse_menu(self, soup, lang):
        accordion_items = soup.find_all("div", class_="fl-accordion-item")
        current_day = datetime.today().weekday()
        menu_details = []
        for item in accordion_items:
            menu_content = item.find("div", class_="fl-accordion-content").find("p")
            menu_html = str(menu_content)
            menu_items = [item.strip() for item in menu_html.split("<br/>") if item.strip()]
            menu_items = [BeautifulSoup(item, "html.parser").text for item in menu_items]
            menu_details.append(menu_items)

        return menu_details[current_day] if menu_details[current_day] else self.fallback_menu[lang]
