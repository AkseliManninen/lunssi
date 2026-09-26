from scrapers.base import RestaurantScraper
import datetime
import re

# Lunch is only served Monday-Friday (weekday(): Mon=0 ... Sun=6)
CLOSED_WEEKDAYS = {5, 6}


class ViatribunaliScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Via Tribunali",
            "https://viatribunali.fi/lounasmenu/",
            "https://maps.app.goo.gl/fMwm6nDwCgLYgZbN9",
            "14€",
            "11:00 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://viatribunali.fi/lounasmenu/",
            "en": "https://viatribunali.fi/en/lunch-menu/",
        }
        self.region = "jatkasaari"

    def parse_menu(self, soup, lang):
        if datetime.date.today().weekday() in CLOSED_WEEKDAYS:
            return self.fallback_menu.get(lang, [])

        menu_items = []

        # Get current week number
        today = datetime.date.today()
        current_week = today.isocalendar()[1]

        week_header = soup.find(
            "h2",
            string=lambda text: (
                text and f"Week {current_week}" in text
                if lang == "en"
                else text and f"Viikko {current_week}" in text
            ),
        )

        if not week_header:
            # Try alternative: find all week sections and get the most recent one
            week_sections = soup.find_all(
                "h2", string=lambda text: text and ("Week" in text or "Viikko" in text)
            )
            if week_sections:
                # Use the first/latest week section
                week_header = week_sections[0]

        if week_header:
            # The week header sits directly inside the page's container div,
            # there is no <section> wrapper around the menu.
            container = week_header.find_parent("div", class_="container") or week_header.parent

            # Find all menu items in the week's container
            menu_divs = container.find_all("div", class_="col-xl-5")

            for menu_div in menu_divs:
                # Extract dish name
                dish_name_elem = menu_div.find("h4")
                if not dish_name_elem:
                    continue

                dish_name = dish_name_elem.get_text(strip=True)

                # Extract price (text is split across nodes, e.g. "14" + "€" in a span)
                price_elem = menu_div.find("p", class_="sdm-3xl--text")
                price = ""
                if price_elem:
                    price = re.sub(r"\s+", "", price_elem.get_text()).rstrip("€")

                # Extract dietary info (Veg, VL, L (G), etc.)
                dietary_elem = menu_div.find("p", class_="sdm--uppercase")
                dietary = dietary_elem.get_text(strip=True) if dietary_elem else ""

                # Extract description: the leftover PDF-to-HTML markup nests the
                # description paragraph inside several layers of empty wrapper
                # divs, so just grab the first <p> that isn't the price/dietary one.
                description = ""
                for p in menu_div.find_all("p"):
                    if p in (price_elem, dietary_elem):
                        continue
                    text = p.get_text(" ", strip=True)
                    if text:
                        description = text
                        break

                # Format the menu item
                item_text = dish_name
                if price:
                    item_text += f" - {price}€"
                if description:
                    item_text += f": {description}"
                if dietary:
                    item_text += f" [{dietary}]"

                menu_items.append(item_text)

        return menu_items if menu_items else self.fallback_menu.get(lang, [])
