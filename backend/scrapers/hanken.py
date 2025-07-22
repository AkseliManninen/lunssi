from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base import RestaurantScraper


class HankenScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Hanken",
            "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=fi",
            "2,80€",
            "11:00 - 15:00",
        )
        self.lang_urls = {
            "fi": "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=fi",
            "en": "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=en",
        }
        self.is_student_cantine = True

    def parse_json_menu(self, data, lang):
        today = datetime.now().date()
        today_menu = None

        for daily_menu in data["MenusForDays"]:
            menu_date = datetime.fromisoformat(daily_menu["Date"].replace("\u002b", "+")).date()
            if menu_date == today:
                today_menu = daily_menu
                break

        if not today_menu or not today_menu["SetMenus"]:
            return self.fallback_menu[lang]

        menu_items = []
        for set_menu in today_menu["SetMenus"]:
            cleaned_components = [
                " ".join(component.split()) for component in set_menu["Components"]
            ]
            menu_line = f"{set_menu['Name']}: {', '.join(cleaned_components)}"
            menu_items.append(menu_line)

        return menu_items if menu_items else self.fallback_menu[lang]

    def get_lunch_info(self, lang="fi", format="json"):
        return super().get_lunch_info(lang, format)
