import httpx
import pymupdf
import re

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
        self.region = "kamppi"
        self.is_student_cantine = False
        self.discount = {
            "fi": "",
            "en": ""
        }

    def get_day_name(self, lang="fi"):
        english_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        finnish_days = [
            "Maanantai",
            "Tiistai",
            "Keskiviikko",
            "Torstai",
            "Perjantai",
            "Lauantai",
            "Sunnuntai",
        ]

        date = datetime.now()
        day_index = date.weekday()

        if lang == "fi":
            return finnish_days[day_index]
        elif lang == "en":
            return english_days[day_index]
        else:
            raise ValueError(f"Language not supported: {lang}")

    async def fetch_html_content(self, lang="fi"):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.lang_urls[lang], headers=self.headers)
            response.raise_for_status()
            return response.content

    async def fetch_json_content(self, lang="fi"):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.lang_urls[lang], headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def fetch_pdf_content(self, url):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.content

    def extract_text_from_pdf(self, pdf_content):
        doc = pymupdf.Document(stream=pdf_content)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    async def get_lunch_info(self, lang="fi", format="html"):
        try:
            if format == "html":
                content = await self.fetch_html_content(lang)
                soup = BeautifulSoup(content, "html.parser")
                menu = self.parse_menu(soup, lang)
            elif format == "pdf":
                if self.url:
                    pdf_content = await self.fetch_pdf_content(self.url)
                    text = self.extract_text_from_pdf(pdf_content)
                    menu = self.parse_pdf_menu(text, lang)
                else:
                    menu = self.fallback_menu[lang]
            elif format == "json":
                content = await self.fetch_json_content(lang)
                menu = self.parse_json_menu(content, lang)
            else:
                raise ValueError("Unsupported format. Use 'html', 'pdf', or 'json'.")
            return (
                self.name,
                menu,
                self.lunch_price,
                self.lunch_available,
                self.is_student_cantine,
                self.discount[lang],
            )
        except Exception as e:
            return (
                self.name,
                self.fallback_menu[lang],
                self.lunch_price,
                self.lunch_available,
                self.is_student_cantine,
                self.discount[lang],
            )


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
                    next_sibling = next_sibling.find_next("div", class_="vc_custom_heading_wrap")
                break

        return menu_items if menu_items else self.fallback_menu[lang]


class KansisScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kansis",
            "https://ravintolakansis.fi/lounas/",
            "12.90 - 14.40€",
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
                parent_div = heading.find_parent("div", class_="wp-block-kadence-dynamichtml")
                if parent_div:
                    for p in parent_div.find_all("p"):
                        menu_text = p.get_text(strip=True)
                        if menu_text:
                            menu_items.append(menu_text)
                break

        return menu_items if menu_items else self.fallback_menu[lang]


class HankenScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Hanken",
            "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=fi",
            "2,80€",
            "11:00 - 15:00",
        )
        self.lang_urls = {
            "fi": "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=fi",
            "en": "https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=en",
        }
        self.is_student_cantine = True

    def parse_json_menu(self, data, lang):
        today = datetime.now().date()
        today_menu = None

        for daily_menu in data["MenusForDays"]:
            menu_date = datetime.fromisoformat(daily_menu["Date"].replace("\u002B", "+")).date()
            if menu_date == today:
                today_menu = daily_menu
                break

        if not today_menu or not today_menu["SetMenus"]:
            return self.fallback_menu[lang]

        menu_items = []
        for set_menu in today_menu["SetMenus"]:
            cleaned_components = [
                " ".join(component.split()) for component in set_menu["Components"]
            ]
            menu_line = f"{set_menu['Name']}: {', '.join(cleaned_components)}"
            menu_items.append(menu_line)

        return menu_items if menu_items else self.fallback_menu[lang]

    def get_lunch_info(self, lang="fi", format="json"):
        return super().get_lunch_info(lang, format)


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
        for heading in soup.find_all("h3"):
            text = heading.get_text(strip=True)
            day = self.get_day_name()
            if day in text:
                next_div = heading.find_next("div")
                next_p = next_div.find_next("p")
                while next_p:
                    if "class" in next_p.attrs and "description" in next_p["class"]:
                        break
                    menu_text = next_p.get_text(separator="\n", strip=True)
                    if menu_text in ["L", "G", "L,G"]:
                        menu_items[-1] = menu_items[-1] + " " + menu_text
                    else:
                        menu_items.append(menu_text)
                    next_p = next_p.find_next("p")
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
        current_day = datetime.today().weekday()
        menu_details = []
        for item in accordion_items:
            menu_content = item.find("div", class_="fl-accordion-content").find("p")
            menu_html = str(menu_content)
            menu_items = [item.strip() for item in menu_html.split("<br/>") if item.strip()]
            menu_items = [BeautifulSoup(item, "html.parser").text for item in menu_items]
            menu_details.append(menu_items)

        return menu_details[current_day] if menu_details[current_day] else self.fallback_menu[lang]


class QueemScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Quê Em",
            "https://queem.fi/menu/lounas/",
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


class StahlbergScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Ståhlberg Tampella",
            "https://www.stahlbergkahvilat.fi/stahlberg-tampella/",
            "13,50€ (Buffet)",
            "10:30 - 15:00",
        )
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        day_id = self.get_day_name().lower()
        day_div = soup.find("div", {"id": day_id})
        if not day_div:
            return self.fallback_menu[lang]

        menu_table = day_div.find("table", {"class": "tablepress"})
        if not menu_table:
            return self.fallback_menu[lang]

        menu_items = []
        for row in menu_table.find_all("tr"):
            cell = row.find("td")
            if cell:
                menu_text = cell.text.strip()
                items = [item.strip() for item in menu_text.split("–") if item.strip()]
                menu_items.extend(items)

        menu_items = list(dict.fromkeys(filter(None, menu_items)))

        return menu_items if menu_items else self.fallback_menu[lang]


class ValssiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Museoravintola Valssi",
            "https://www.vapriikki.fi/vieraile/museoravintola-valssi/lounaslista/",
            "11,90€",
            "10:45 - 14:00",
        )
        self.region = "tampere"

    def parse_menu(self, soup, lang):
        menu_container = soup.find(
            "div", class_="column is-6 is-offset-3 pt-0 pb-0 has-text-centered"
        )
        if not menu_container:
            return self.fallback_menu[lang]
        today = datetime.today()
        today_date = today.strftime("%-d.%-m.")
        day_sections = menu_container.find_all("div", class_="", recursive=False)
        for section in day_sections:
            day_header = section.find("h3", class_="h3")
            if not day_header:
                continue
            date_match = re.search(r"\d{1,2}\.\d{1,2}\.", day_header.text)
            if not date_match:
                continue
            menu_date = date_match.group()
            if menu_date == today_date:
                mt5_divs = section.find_all("div", class_="mt-5")
                if len(mt5_divs) < 2:
                    continue
                menu_content = mt5_divs[1].find("p")
                if not menu_content:
                    continue
                menu_items = []
                for br in menu_content.find_all("<br>"):
                    br.replace_with("\n")
                menu_text = menu_content.get_text()
                for item in menu_text.split("\n"):
                    item = item.strip()
                    if item:
                        menu_items.append(item)
                return menu_items
        return self.fallback_menu[lang]

class FaasaiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Faasai Koskikatu",
            "https://www.faasairavintola.fi/koskikatu.html",
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

class KarljohanScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Karljohan",
            "https://www.ravintolakarljohan.fi/lounas-fi/lounas/",
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


def get_restaurants_by_region(region="kamppi"):
    all_scrapers = {
        "bruuveri": BruuveriScraper(),
        "hanken": HankenScraper(),
        "hämis": HamisScraper(),
        "kansis": KansisScraper(),
        "karljohan": KarljohanScraper(),
        "plaza": PlazaScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "queem": QueemScraper(),
        "stahlberg": StahlbergScraper(),
        "valssi": ValssiScraper(),
        "faasai": FaasaiScraper(),
    }
    return {name: scraper for name, scraper in all_scrapers.items() if scraper.region == region}


def get_lunch_info(restaurant_shorthand, region="kamppi", lang="fi"):
    scrapers_region = get_restaurants_by_region(region)
    scraper = scrapers_region.get(restaurant_shorthand.lower())
    if scraper:
        return scraper.get_lunch_info(lang)
    else:
        return f"No scraper found for restaurant: {restaurant_shorthand}"
