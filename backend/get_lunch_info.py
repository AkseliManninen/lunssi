import requests
from bs4 import BeautifulSoup
from datetime import datetime


class RestaurantScraper:
    def __init__(self, name, url, lunch_price, lunch_available):
        self.name = name
        self.url = url
        self.lunch_price = lunch_price
        self.lunch_available = lunch_available
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.date_str = datetime.now().strftime("%-d.%-m")

    def fetch_html_content(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.content

    def get_lunch_info(self):
        try:
            html_content = self.fetch_html_content()
            soup = BeautifulSoup(html_content, "html.parser")
            menu = self.parse_menu(soup)
            return menu, self.lunch_price, self.lunch_available
        except Exception as e:
            return f"Virhe: {str(e)}"


class BruuveriScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bruuveri",
            "https://www.bruuveri.fi/lounas-menu/",
            "14,50€ (Noutopöytä), 13€ (Kevytlounas)",
            "11:00 - 14:00",
        )

    def parse_menu(self, soup):
        menu_items = []
        for menu in soup.find_all("div", class_="heading-text"):
            text = menu.get_text(strip=True)
            if self.date_str in text:
                next_sibling = menu.find_next("div", class_="vc_custom_heading_wrap")
                while next_sibling:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    if any(char.isdigit() for char in menu_text):
                        break
                    menu_items.append(menu_text)
                    next_sibling = next_sibling.find_next(
                        "div", class_="vc_custom_heading_wrap"
                    )
                break

        return (
            "\n".join(menu_items)
            if menu_items
            else f"Lounasta ei saatavilla {self.date_str}"
        )


class KansisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kansis",
            "https://ravintolakansis.fi/lounas/",
            "12.70 - 14.20€",
            "11:00 - 14:00",
        )

    def parse_menu(self, soup):
        menu_items = []
        for heading in soup.find_all("h3"):
            text = heading.get_text(strip=True)
            if self.date_str in text:
                parent_div = heading.find_parent()
                next_sibling = heading.find_next_sibling()
                while next_sibling and next_sibling in parent_div:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    menu_items.append(menu_text)
                    next_sibling = next_sibling.find_next_sibling()
                break

        return (
            "\n".join(menu_items)
            if menu_items
            else f"Lounasta ei saatavilla {self.date_str}"
        )


class PompierAlbertinkatuScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Pompier Albertinkatu",
            "https://pompier.fi/albertinkatu/albertinkatu-menu/",
            "14 - 19€",
            "10:45 - 14:00 Arkisin",
        )

    def parse_menu(self, soup):
        accordion_items = soup.find_all("div", class_="fl-accordion-item")
        menu_details = {}
        for item in accordion_items:
            day = item.find("a", class_="fl-accordion-button-label").text.strip()
            menu = (
                item.find("div", class_="fl-accordion-content").find("p").text.strip()
            )
            menu_details[day] = menu

        menu_items = next(
            (menu for day, menu in menu_details.items() if self.date_str in day), None
        )
        return menu_items if menu_items else f"Lounasta ei saatavilla {self.date_str}"


class HamisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Hämis",
            "https://hys.net/osakuntabaari/ruokalista/",
            "2,95€",
            "11:00 - 15:00",
        )

    def parse_menu(self, soup):
        today_row = soup.find("div", class_="row row-today")
        if today_row:
            menu_items = (
                today_row.find("div", class_="col-food").text.strip().split("\n")
            )
            return "\n".join(menu_items)
        else:
            return "Today's menu not found."


def get_lunch_info(restaurant_name):
    scrapers = {
        "bruuveri": BruuveriScraper(),
        "kansis": KansisScraper(),
        "pompier-albertinkatu": PompierAlbertinkatuScraper(),
        "hämis": HamisScraper(),
    }
    scraper = scrapers.get(restaurant_name.lower())
    if scraper:
        return scraper.get_lunch_info()
    else:
        return f"No scraper found for restaurant: {restaurant_name}"
