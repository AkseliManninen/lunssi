import re

from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base import RestaurantScraper


class ValssiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Museoravintola Valssi",
            "https://www.vapriikki.fi/vieraile/museoravintola-valssi/lounaslista/",
            "11,90€",
            "10:45 - 14:00",
        )
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        menu_container = soup.find(
            "div", class_="column is-6 is-offset-3 pt-0 pb-0 has-text-centered"
        )
        if not menu_container:
            return self.fallback_menu[lang]
        today = datetime.today()
        today_date = today.strftime("%-d.%-m.")
        day_sections = menu_container.find_all("div", class_="", recursive=False)
        for section in day_sections:
            day_header = section.find("h3", class_="h3")
            if not day_header:
                continue
            date_match = re.search(r"\d{1,2}\.\d{1,2}\.", day_header.text)
            if not date_match:
                continue
            menu_date = date_match.group()
            if menu_date == today_date:
                mt5_divs = section.find_all("div", class_="mt-5")
                if len(mt5_divs) < 2:
                    continue
                menu_content = mt5_divs[1].find("p")
                if not menu_content:
                    continue
                menu_items = []
                for br in menu_content.find_all("<br>"):
                    br.replace_with("\n")
                menu_text = menu_content.get_text()
                for item in menu_text.split("\n"):
                    item = item.strip()
                    if item:
                        menu_items.append(item)
                return menu_items
        return self.fallback_menu[lang]
