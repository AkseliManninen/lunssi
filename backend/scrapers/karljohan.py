from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class KarljohanScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Karljohan",
            "https://www.ravintolakarljohan.fi/lounas-fi/lounas/",
            "https://maps.app.goo.gl/eH9CmRTSSFZCRAzh8",
            "13,70 - 25€",
            "10:30 - 15:00",
        )

    def parse_menu(self, soup: BeautifulSoup, lang: str):
        # Check if the menu is for today
        date_heading = soup.find("h2", class_="elementor-heading-title")
        if date_heading:
            current_day = self.get_day_name().lower()
            heading_text = date_heading.text.strip().lower()
            if current_day not in heading_text:
                return self.fallback_menu[lang]

        menu_items = []
        items = soup.find_all("div", class_="wpr-price-list-item")
        for item in items:
            title = item.find("span", class_="wpr-price-list-title")
            price = item.find("span", class_="wpr-price-list-price")
            description = item.find("div", class_="wpr-price-list-description")

            if title and price:
                title_text = title.text.strip()
                price_text = price.text.strip()
                desc_text = description.text.strip() if description else ""
                menu_item = f"{title_text} {price_text}"
                if desc_text:
                    menu_item += f" {desc_text}"

                menu_items.append(menu_item)

        return menu_items if menu_items else self.fallback_menu[lang]
