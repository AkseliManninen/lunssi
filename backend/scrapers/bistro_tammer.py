from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base import RestaurantScraper


class BistroTammerScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bistro Tammer",
            "https://www.raflaamo.fi/fi/ravintola/tampere/bistro-tammer/menu/lounas",
            "https://maps.app.goo.gl/s9TVqXzCEFHiQUBd6",
            "13,70€ (Soup), 15,50€ (Buffet)",
            "11:00 - 13:00",
        )
        self.lang_urls = {
            "fi": "https://www.raflaamo.fi/fi/rav<intola/tampere/bistro-tammer/menu/lounas",
            "en": "https://www.raflaamo.fi/en/restaurant/tampere/bistro-tammer/menu/lunch",
        }
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        today_en = datetime.now().strftime("%d/%m")
        today_fi = f"{datetime.now().day}.{datetime.now().month}."
        menu_items = []
        day_header = None
        for h in soup.find_all("h3"):
            print("Otskikko:\n")
            print(h)
            if today_en in h or today_fi in h:
                day_header = h
                print("Day header:", h)
                break
        if not day_header:
            return self.fallback_menu.get(lang, [])
        container = day_header.find_parent("div")
        while container and not container.find("ul"):
            container = container.find_next_sibling("div")
        if not container:
            return self.fallback_menu.get(lang, [])
        for li in container.find_all("li"):
            name_tag = li.find("span")
            name = name_tag.get_text(strip=True) if name_tag else ""
            diet_tags = [tag.get("title") for tag in li.find_all("span") if tag.has_attr("title")]
            diet_str = f" ({', '.join(diet_tags)})" if diet_tags else ""
            desc_tag = li.find("p")
            description = desc_tag.get_text(strip=True) if desc_tag else ""
            full_item = f"{name}{diet_str}"
            if description:
                full_item += f",\n{description}"
            menu_items.append(full_item)
        return menu_items if menu_items else self.fallback_menu.get(lang, [])
