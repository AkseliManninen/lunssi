from scrapers.base import RestaurantScraper
import re
import datetime


class KansisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kansis",
            "https://ravintolakansis.fi/lounas/",
            "https://maps.app.goo.gl/mbjMPQnfLZEYHobS9",
            "12.90 - 14.40€",
            "11:00 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://ravintolakansis.fi/lounas/",
            "en": "https://ravintolakansis.fi/lunchkamppi/",
        }

    def parse_menu(self, soup, lang):
        menu_items = []

        today = datetime.date.today()
        weekday = self.get_day_name(lang)
        month_name = today.strftime("%B")
        pattern_str = ""

        if lang == "fi":
            pattern_str = rf"{weekday}\s+{today.day}\.\s*{today.month}\.?"
        elif lang == "en":
            pattern_str = rf"{weekday},*\s+{month_name}\s+{today.day}\.?"

        date_pattern = re.compile(pattern_str, re.IGNORECASE)
        date_element = soup.find(string=date_pattern)

        if date_element:
            parent_div = date_element.find_parent("div", class_="wp-block-kadence-dynamichtml")

            if parent_div:
                for p in parent_div.find_all("p"):
                    menu_text = p.get_text(strip=True)
                    if menu_text and not date_pattern.search(menu_text):
                        menu_items.append(menu_text)

        return menu_items if menu_items else self.fallback_menu.get(lang, [])
