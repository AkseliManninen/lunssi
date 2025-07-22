from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class PlazaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Plaza",
            "https://www.ardenrestaurants.fi/menut/plaza/index.php",
            "14,50€",
            "10:30 - 14:00",
        )

    def parse_menu(self, soup, lang):
        menu_items = []
        for heading in soup.find_all("h3"):
            text = heading.get_text(strip=True)
            day = self.get_day_name()
            if day in text:
                next_div = heading.find_next("div")
                next_p = next_div.find_next("p")
                while next_p:
                    if "class" in next_p.attrs and "description" in next_p["class"]:
                        break
                    menu_text = next_p.get_text(separator="\n", strip=True)
                    if menu_text in ["L", "G", "L,G"]:
                        menu_items[-1] = menu_items[-1] + " " + menu_text
                    else:
                        menu_items.append(menu_text)
                    next_p = next_p.find_next("p")
                break
        return menu_items if menu_items else self.fallback_menu[lang]
