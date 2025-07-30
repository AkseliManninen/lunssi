from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class StahlbergScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Ståhlberg Tampella",
            "https://www.stahlbergkahvilat.fi/stahlberg-tampella/",
            "https://maps.app.goo.gl/G4tBvRLy1q3VZCns5",
            "13,50€ (Buffet)",
            "10:30 - 15:00",
        )
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        day_id = self.get_day_name().lower()
        day_div = soup.find("div", {"id": day_id})
        if not day_div:
            return self.fallback_menu[lang]

        menu_table = day_div.find("table", {"class": "tablepress"})
        if not menu_table:
            return self.fallback_menu[lang]

        menu_items = []
        for row in menu_table.find_all("tr"):
            cell = row.find("td")
            if cell:
                menu_text = cell.text.strip()
                items = [item.strip() for item in menu_text.split("–") if item.strip()]
                menu_items.extend(items)

        menu_items = list(dict.fromkeys(filter(None, menu_items)))

        return menu_items if menu_items else self.fallback_menu[lang]
