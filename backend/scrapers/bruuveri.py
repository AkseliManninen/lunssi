from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class BruuveriScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bruuveri",
            "https://www.bruuveri.fi/lounas-menu/",
            "14,50€ (Buffet), 13€ (Light lunch)",
            "11:00 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://www.bruuveri.fi/lounas-menu/",
            "en": "https://www.bruuveri.fi/en/lounas-menu/",
        }

    def parse_menu(self, soup, lang):
        menu_items = []
        for menu in soup.find_all("div", class_="heading-text"):
            text = menu.get_text(strip=True)
            if self.date_str in text:
                next_sibling = menu.find_next("div", class_="vc_custom_heading_wrap")
                while next_sibling:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    if any(char.isdigit() for char in menu_text):
                        break
                    items = menu_text.split("\n")
                    menu_items.extend(items)
                    next_sibling = next_sibling.find_next("div", class_="vc_custom_heading_wrap")
                break

        return menu_items if menu_items else self.fallback_menu[lang]
