from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class BruuveriScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Bruuveri",
            "https://bruuveri.fi/lounas/",
            "https://maps.app.goo.gl/12KwLxcWQpDfnMAYA",
            "14€ - 16€",
            "10:30 - 14:30",
        )

    def is_day_heading(self, element, day=None):
        if element.name not in ("strong", "h2", "h3", "h4"):
            return False
        text = element.get_text(strip=True).lower()
        days = (day,) if day else self.finnish_days
        return any(text.startswith(d.lower()) for d in days)

    def parse_menu(self, soup, lang):
        day = self.get_day_name().lower()
        heading = soup.find(lambda tag: self.is_day_heading(tag, day))
        if heading is None:
            return self.menu_fallback[lang]

        # Days are either wrapped in a container or flat siblings, so take the
        # first list or paragraph after the heading, unless another day heading
        # comes first. Paragraphs hold one dish per line, separated by <br>.
        menu_items = []
        for element in heading.next_elements:
            if getattr(element, "name", None) is None:
                continue
            if self.is_day_heading(element):
                break
            if element.name == "ul":
                menu_items = [li.get_text(strip=True) for li in element.find_all("li")]
                break
            if element.name == "p" and element.get_text(strip=True):
                menu_items = element.get_text("\n", strip=True).split("\n")
                break

        return menu_items if menu_items else self.menu_fallback[lang]
