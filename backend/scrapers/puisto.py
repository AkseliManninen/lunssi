from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base import RestaurantScraper


class PuistoScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Puisto",
            "https://www.raflaamo.fi/fi/ravintola/tampere/puisto/menu/lounas",
            "https://maps.app.goo.gl/svbC5hrvCpxYr2HD8",
            "13,50 - 14,90€",
            "11:00 - 14:30",
        )
        self.lang_urls = {
            "en": "https://www.raflaamo.fi/en/restaurant/tampere/puisto/menu/lunch",
            "fi": "https://www.raflaamo.fi/fi/ravintola/tampere/puisto/menu/lounas",
        }
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        today_en = datetime.now().strftime("%d/%m")
        today_fi = f"{datetime.now().day}.{datetime.now().month}."

        day_header = None
        for h in soup.find_all("h3"):
            if today_fi in h.get_text() or today_en in h.get_text():
                day_header = h
                break
        if not day_header:
            return self.fallback_menu[lang]

        container = day_header.find_parent("div")
        while container and not container.find("ul"):
            container = container.find_next_sibling("div")
        if not container:
            return self.fallback_menu[lang]

        menu_lines = []
        for li in container.find_all("li"):
            name_tag = li.find("span")
            name = name_tag.get_text(strip=True) if name_tag else ""
            desc_tag = li.find("p")
            description = desc_tag.get_text(strip=True) if desc_tag else ""
            line = f"{name}: {description}" if description else name
            if line:
                menu_lines.append(line)
        return menu_lines if menu_lines else self.fallback_menu[lang]
