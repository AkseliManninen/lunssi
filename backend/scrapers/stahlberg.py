from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class StahlbergScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Ståhlberg Tampella",
            "https://stahlbergkahvilat.fi/lounasravintolat/tampella/",
            "https://maps.app.goo.gl/G4tBvRLy1q3VZCns5",
            "13,90€ (Buffet)",
            "10:30 - 15:00",
        )
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        day_name = self.get_day_name().lower()
        day_heading = soup.find(
            "h3", string=lambda text: text and text.strip().lower().startswith(day_name)
        )
        if not day_heading:
            return self.menu_fallback[lang]

        menu_table = day_heading.find_next("table", class_="ruokalista")
        if not menu_table:
            return self.menu_fallback[lang]

        menu_items = []
        for row in menu_table.find_all("tr"):
            cell = row.find("td")
            if cell:
                menu_text = cell.text.strip()
                items = [item.strip() for item in menu_text.split("–") if item.strip()]
                menu_items.extend(items)

        menu_items = list(dict.fromkeys(filter(None, menu_items)))

        return menu_items if menu_items else self.menu_fallback[lang]
