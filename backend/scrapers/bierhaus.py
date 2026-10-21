from datetime import datetime

from scrapers.base import RestaurantScraper


class BierhausScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bierhaus",
            "https://www.bierhaus.fi/menut/kamppi/index.html#viikon-lounas",
            "https://maps.app.goo.gl/idZc7S8n4pU6dztH7",
            "14,80€",
            "10:30 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://www.bierhaus.fi/menut/kamppi/index.html",
            "en": "https://www.bierhaus.fi/en/menus/kamppi/index.html",
        }

    def parse_menu(self, soup, lang):
        menu_items = []
        today = datetime.now().strftime("%-d.%-m.%Y")
        for day in soup.select("article.menu-day"):
            date = day.select_one(".menu-day-date")
            if not date or date.get_text(strip=True) != today:
                continue
            for row in day.select("li.menu-row"):
                name = row.select_one(".menu-name").get_text(strip=True)
                marks = row.select_one(".menu-marks")
                raw_marks = row.select_one(".menu-marks-raw")
                if marks:
                    name += " " + ", ".join(
                        abbr.get_text(strip=True) for abbr in marks.find_all("abbr")
                    )
                elif raw_marks:
                    name += " " + raw_marks.get_text(strip=True)
                menu_items.append(name)
            break
        return menu_items if menu_items else self.menu_fallback[lang]
