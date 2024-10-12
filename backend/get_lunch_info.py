import pymupdf
import re
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

    def get_day_name(self, lang="fi"):
        english_days = [
            "Monday", "Tuesday", "Wednesday", 
            "Thursday", "Friday", "Saturday", "Sunday"
        ]
        
        finnish_days = [
            "Maanantai", "Tiistai", "Keskiviikko", 
            "Torstai", "Perjantai", "Lauantai", "Sunnuntai"
        ]
        
        date = datetime.now()
        day_index = date.weekday()
        
        if lang == "fi":
            return finnish_days[day_index]
        elif lang == "en":
            return english_days[day_index]
        else:
            raise ValueError(f"Language not supported: {lang}")

    def fetch_html_content(self, lang="fi"):
        response = requests.get(self.lang_urls[lang], headers=self.headers)
        response.raise_for_status()
        return response.content

    def fetch_pdf_content(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.content
        return data

    def extract_text_from_pdf(self, pdf_content):
        doc = pymupdf.Document(stream=pdf_content)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def get_lunch_info(self, lang="fi", format="html"):
        try:
            if format == "html":
                content = self.fetch_html_content(lang)
                soup = BeautifulSoup(content, "html.parser")
                menu = self.parse_menu(soup, lang)
            elif format == "pdf":
                pdf_content = self.fetch_pdf_content(self.url)
                text = self.extract_text_from_pdf(pdf_content)
                menu = self.parse_pdf_menu(text, lang)
            else:
                raise ValueError("Unsupported format. Use 'html' or 'pdf'.")

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


class PlazaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Plaza",
            "https://www.ardenrestaurants.fi/menut/plaza/index.php",
            "14,50€",
            "10:30 - 14:00",
        ) 

    def parse_menu(self, soup, lang):
        menu_items = []
        for heading in soup.find_all('h3'):
            text = heading.get_text(strip=True)
            day = self.get_day_name()
            if day in text:
                next_div = heading.find_next('div')
                next_p = next_div.find_next('p')
                while next_p:
                    if 'class' in next_p.attrs and 'description' in next_p['class']:
                        break
                    menu_text = next_p.get_text(separator="\n", strip=True)
                    if menu_text in ["L", "G", "L,G"]:
                        menu_items[-1] = menu_items[-1] + " " + menu_text
                    else:
                        menu_items.append(menu_text)
                    next_p = next_p.find_next('p')
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


class QueemScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Quê Em",
            "https://queem.fi/wp-content/uploads/2024/09/",
            "13,50€ - 16,90€",
            "11:00 - 14:00",
        )

    def get_pdf_url(self):
        today = datetime.now()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_of_week = days[today.weekday()]
        return f"{self.url}{day_of_week}-lunch-29.7-uudistettu.pdf"

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

    def get_lunch_info(self, lang="fi", format="pdf"):
        self.url = self.get_pdf_url()
        return super().get_lunch_info(lang, format)


def get_lunch_info(restaurant_shorthand, lang="fi"):
    scrapers = {
        "bruuveri": BruuveriScraper(),
        "kansis": KansisScraper(),
        "plaza": PlazaScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "hämis": HamisScraper(),
        "queem": QueemScraper(),
    }
    scraper = scrapers.get(restaurant_shorthand.lower())
    if scraper:
        return scraper.get_lunch_info(lang)
    else:
        return f"No scraper found for restaurant: {restaurant_shorthand}"
