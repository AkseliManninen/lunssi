import requests

from bs4 import BeautifulSoup
from datetime import datetime


class RestaurantScraper:
    def __init__(self, name, url, lunch_price, lunch_available):
        self.date_str = datetime.now().strftime("%-d.%-m")
        self.fallback_menu = {
            "fi": ["Tämän päivän lounasta ei löytynyt."],
            "en": ["Today's lunch menu not found."],
        }
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.name = name
        self.lunch_available = lunch_available
        self.lunch_price = lunch_price
        self.url = url
        # Default to same URL for both languages
        self.lang_urls = {
            "fi": url,
            "en": url,
        }

    def fetch_html_content(self, lang="fi"):
        response = requests.get(self.lang_urls[lang], headers=self.headers)
        response.raise_for_status()
        return response.content

    def get_lunch_info(self, lang="fi"):
        try:
            html_content = self.fetch_html_content(lang)
            soup = BeautifulSoup(html_content, "html.parser")
            menu = self.parse_menu(soup, lang)
            return self.name, menu, self.lunch_price, self.lunch_available
        except Exception as e:
            return f"Error: {str(e)}"


class BruuveriScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bruuveri",
            "https://www.bruuveri.fi/lounas-menu/",
            "14,50€ (Buffet), 13€ (Light lunch)",
            "11:00 - 14:00",
        )
        self.lang_urls = {
            "fi": "https://www.bruuveri.fi/lounas-menu/",
            "en": "https://www.bruuveri.fi/en/lounas-menu/",
        }

    def parse_menu(self, soup, lang):
        menu_items = []
        for menu in soup.find_all("div", class_="heading-text"):
            text = menu.get_text(strip=True)
            if self.date_str in text:
                next_sibling = menu.find_next("div", class_="vc_custom_heading_wrap")
                while next_sibling:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    if any(char.isdigit() for char in menu_text):
                        break
                    items = menu_text.split("\n")
                    menu_items.extend(items)
                    next_sibling = next_sibling.find_next(
                        "div", class_="vc_custom_heading_wrap"
                    )
                break

        return menu_items if menu_items else self.fallback_menu[lang]


class KansisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kansis",
            "https://ravintolakansis.fi/lounas/",
            "12.70 - 14.20€",
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
                parent_div = heading.find_parent()
                next_sibling = heading.find_next_sibling()
                while next_sibling and next_sibling in parent_div:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    if menu_text:
                        menu_items.append(menu_text)
                    next_sibling = next_sibling.find_next_sibling()
                break

        return menu_items if menu_items else self.fallback_menu[lang]


class PompierAlbertinkatuScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Pompier Albertinkatu",
            "https://pompier.fi/albertinkatu/albertinkatu-menu/",
            "14 - 19€",
            "10:45 - 14:00",
        )

    def parse_menu(self, soup, lang):
        accordion_items = soup.find_all("div", class_="fl-accordion-item")
        menu_details = {}
        for item in accordion_items:
            day = item.find("a", class_="fl-accordion-button-label").text.strip()
            menu_content = item.find("div", class_="fl-accordion-content").find("p")
            menu_html = str(menu_content)
            menu_items = [
                item.strip() for item in menu_html.split("<br/>") if item.strip()
            ]
            menu_items = [
                BeautifulSoup(item, "html.parser").text for item in menu_items
            ]
            menu_details[day] = menu_items

        return menu_items if menu_items else self.fallback_menu[lang]


class HamisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Hämäläis-Osakunta",
            "https://hys.net/osakuntabaari/ruokalista/",
            "2,95€",
            "11:00 - 15:00",
        )

    def parse_menu(self, soup, lang):
        today_row = soup.find("div", class_="row row-today")
        if today_row:
            menu_div = today_row.find("div", class_="col-food")
            menu_html = str(menu_div.p)
            menu_items = [
                item.strip() for item in menu_html.split("<br/>") if item.strip()
            ]
            menu_items = [
                BeautifulSoup(item, "html.parser").text for item in menu_items
            ]
            return menu_items
        else:
            return self.fallback_menu[lang]


def get_lunch_info(restaurant_shorthand, lang="fi"):
    scrapers = {
        "bruuveri": BruuveriScraper(),
        "kansis": KansisScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "hämis": HamisScraper(),
    }
    scraper = scrapers.get(restaurant_shorthand.lower())
    if scraper:
        return scraper.get_lunch_info(lang)
    else:
        return f"No scraper found for restaurant: {restaurant_shorthand}"
