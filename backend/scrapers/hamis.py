from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class HamisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Hämäläis-Osakunta",
            "https://hys.net/osakuntabaari/ruokalista/",
            "2,95€",
            "11:00 - 15:00",
        )
        self.is_student_cantine = True

    def parse_menu(self, soup, lang):
        today_row = soup.find("div", class_="row row-today")
        if today_row:
            menu_div = today_row.find("div", class_="col-food")
            menu_html = str(menu_div.p)
            menu_items = [item.strip() for item in menu_html.split("<br/>") if item.strip()]
            menu_items = [BeautifulSoup(item, "html.parser").text for item in menu_items]
            return menu_items
        else:
            return self.fallback_menu[lang]
