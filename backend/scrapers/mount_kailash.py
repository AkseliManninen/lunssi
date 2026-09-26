from scrapers.base import RestaurantScraper
import re


class MountKailashScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Mount Kailash",
            "https://mountkailash.fi/lunch-menu",
            "https://www.google.com/maps/search/?api=1&query=Mount+Kailash+Restaurant+J%C3%A4tk%C3%A4saari",
            "13,70€ - 18,90€",
            "10:30 - 15:00",
        )
        self.lang_urls = {
            "fi": "https://mountkailash.fi/lunch-menu",
            "en": "https://mountkailash.fi/lunch-menu",
        }
        self.region = "jatkasaari"

    def parse_menu(self, soup, lang):
        menu_items = []
        today_name = self.get_day_name("fi").upper()
        # Each day has two columns (lm-col-left / lm-col-right) sharing the
        # same "<FI> / <EN>" title, e.g. "MAANANTAI / MONDAY".
        col_titles = soup.find_all(
            "div",
            class_="lm-col-title",
            string=lambda text: text and today_name in text,
        )

        for col_title in col_titles:
            column = col_title.find_parent("div", class_=re.compile(r"lm-col-(left|right)"))
            if not column:
                continue

            for item in column.find_all("div", class_="lm-item"):
                name_span = item.find("span", id=re.compile(r"^menu_"))
                if not name_span:
                    continue
                name = " ".join(name_span.get_text(strip=True).split())

                tags = [tag.get_text(strip=True) for tag in item.find_all("span", class_="lm-tag")]

                price_elem = item.find("span", class_="lm-item-price")
                price = price_elem.get_text(strip=True) if price_elem else ""

                desc_class = "d-fi" if lang == "fi" else "d-en"
                desc_elem = item.find("span", class_=desc_class)
                description = " ".join(desc_elem.get_text(strip=True).split()) if desc_elem else ""

                item_text = f"{name} ({', '.join(tags)})" if tags else name
                if description:
                    item_text += f": {description}"
                if price:
                    item_text += f" - {price}"

                menu_items.append(item_text)

        return menu_items if menu_items else self.menu_fallback[lang]
