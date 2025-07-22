from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class KansisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kansis",
            "https://ravintolakansis.fi/lounas/",
            "12.90 - 14.40€",
            "11:00 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://ravintolakansis.fi/lounas/",
            "en": "https://ravintolakansis.fi/lunchkamppi/",
        }

    def parse_menu(self, soup, lang):
        menu_items = []
        for heading in soup.find_all("h3"):
            text = heading.get_text(strip=True)
            if self.date_str in text:
                parent_div = heading.find_parent("div", class_="wp-block-kadence-dynamichtml")
                if parent_div:
                    for p in parent_div.find_all("p"):
                        menu_text = p.get_text(strip=True)
                        if menu_text:
                            menu_items.append(menu_text)
                break

        return menu_items if menu_items else self.fallback_menu[lang]
