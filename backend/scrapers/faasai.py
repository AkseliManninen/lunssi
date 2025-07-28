from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class FaasaiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Faasai Koskikatu",
            "https://www.faasairavintola.fi/koskikatu.html",
            "https://maps.app.goo.gl/Ec949wqMiJvJX7v4A",
            "13,50€",
            "11:00 - 15:00",
        )
        self.region = "tampere"
        self.discount = {
            "fi": "1€ alennus lounaasta, kun tiskillä mainitsee Futuricen",
            "en": "1€ discount on lunch when mentioning Futurice at the counter",
        }

    def parse_menu(self, soup, lang):
        paragraphs = soup.find_all("p")
        menu_item = []

        if not paragraphs:
            return self.fallback_menu[lang]

        # Find the paragraph from paragraphs that contains "Perinteinen Faasain thaimaalainen"
        for paragraph in paragraphs:
            if "Perinteinen Faasain thaimaalainen" in paragraph.text:
                menu_item = paragraph.text.split("\n")

        return menu_item
