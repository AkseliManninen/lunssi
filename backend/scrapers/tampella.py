from datetime import datetime
from scrapers.base import RestaurantScraper


class TampellaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Ravintola Tampella",
            "https://www.ravintolatampella.fi/lounas/",
            "https://maps.app.goo.gl/zrHCSHhTLe3P1ASU8",
            "14,00 - 21,90€",
            "11:00 - 14:00",
        )
        # The lunch page embeds a Lounastaja widget; its API returns all languages at once.
        api_url = "https://lounastaja.app/api/v1/widget/5612c69a-7702-4ac0-b1b7-c63de8a77603/7ltuWbVejyOCDjRzzMTf"
        self.lang_urls = {
            "fi": api_url,
            "en": api_url,
        }
        self.region = "tampere"

    def parse_json_menu(self, data, lang):
        today = datetime.now().strftime("%Y-%m-%d")
        days = data["data"]["week"]["days"]
        today_menu = next((day for day in days if day["dateString"] == today), None)
        if not today_menu or today_menu["isClosed"]:
            return self.menu_fallback[lang]

        menu_items = []
        for lunch in today_menu["lunches"]:
            # Skip the fixed à la carte dishes that are listed every day
            if lunch["isWeekMenuLunch"]:
                continue
            title = lunch["title"].get(lang) or lunch["title"]["fi"]
            if not title:
                continue
            allergens = [
                a["abbreviation"].get(lang) or a["abbreviation"]["fi"] for a in lunch["allergens"]
            ]
            menu_items.append(f"{title} ({', '.join(allergens)})" if allergens else title)

        return menu_items if menu_items else self.menu_fallback[lang]

    def get_lunch_info(self, lang="fi", format="json"):
        return super().get_lunch_info(lang, format)
