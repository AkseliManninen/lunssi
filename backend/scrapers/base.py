import httpx
import pymupdf

from bs4 import BeautifulSoup
from datetime import datetime


class RestaurantScraper:
    def __init__(self, name, url, location, lunch_price, lunch_available):
        self.date_str = datetime.now().strftime("%-d.%-m")
        self.discount = {"fi": "", "en": ""}
        self.fallback_menu = {
            "fi": ["Tämän päivän lounasta ei löytynyt."],
            "en": ["Today's lunch menu not found."],
        }
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.is_student_cantine = False
        self.lang_urls = {
            "fi": url,
            "en": url,
        }
        self.location = location
        self.lunch_available = lunch_available
        self.lunch_price = lunch_price
        self.name = name
        self.region = "kamppi"
        self.url = url

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
        day_index = datetime.now().weekday()
        return finnish_days[day_index] if lang == "fi" else english_days[day_index]

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
        return "".join([page.get_text() for page in doc])

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
                raise ValueError("Unsupported format.")
            return (
                self.name,
                menu,
                self.lunch_price,
                self.lunch_available,
                self.is_student_cantine,
                self.discount[lang],
            )
        except Exception:
            return (
                self.name,
                self.fallback_menu[lang],
                self.lunch_price,
                self.lunch_available,
                self.is_student_cantine,
                self.discount[lang],
            )
