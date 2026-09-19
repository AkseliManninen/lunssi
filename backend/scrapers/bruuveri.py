from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class BruuveriScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bruuveri",
            "https://bruuveri.fi/lounas/",
            "https://maps.app.goo.gl/12KwLxcWQpDfnMAYA",
            "14€ - 16€",
            "10:30 - 14:30",
        )

    def parse_menu(self, soup, lang):
        day_id = self.get_day_name().lower()
        day_div = soup.find("div", id=day_id)
        if day_div is None:
            return self.fallback_menu[lang]

        list_items = day_div.find_all("li")
        if list_items:
            menu_items = [item.get_text(strip=True) for item in list_items]
        else:
            desc = day_div.find("div", class_="uagb-ifb-desc")
            menu_text = desc.get_text(separator="\n", strip=True) if desc else ""
            menu_items = [line for line in menu_text.split("\n") if line]

        return menu_items if menu_items else self.fallback_menu[lang]
