import re

from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class QueemScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Quê Em",
            "https://queem.fi/menu/lounas/",
            "https://maps.app.goo.gl/aKbHnw472ULKRTFu8",
            "13,50€ - 16,90€",
            "11:00 - 14:00",
        )

    async def get_pdf_url(self):
        content = await self.fetch_html_content(lang="fi")
        soup = BeautifulSoup(content, "html.parser")

        today_finnish = self.get_day_name(lang="fi")

        menu_links = soup.find_all("a", class_="wp-block-button__link")

        for link in menu_links:
            if today_finnish in link.text:
                if link.get("href"):
                    return link["href"]
        return None

    def parse_pdf_menu(self, text, lang):
        lines = text.split("\n")
        lunch_items = []
        current_item = None
        current_lines = []
        for line in lines:
            line = line.strip()
            if re.match(r"^\d+\.", line):
                if current_item:
                    lunch_items.append(" ".join([current_item] + current_lines))
                current_item = line
                current_lines = []
            elif line and current_item is not None:
                current_lines.append(line)
        if current_item:
            lunch_items.append(" ".join([current_item] + current_lines))

        return lunch_items if lunch_items else self.fallback_menu[lang]

    async def get_lunch_info(self, lang="fi", format="pdf"):
        self.url = await self.get_pdf_url()
        return await super().get_lunch_info(lang, format)
