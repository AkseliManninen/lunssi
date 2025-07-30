import httpx
import pymupdf

from bs4 import BeautifulSoup
from datetime import datetime


class RestaurantScraper:
    def __init__(self, name, url, location, lunch_price, lunch_hours):
        self.date_str = datetime.now().strftime("%-d.%-m")
        self.discount = {"fi": "", "en": ""}
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.is_student_cantine = False
        self.lang_urls = {
            "fi": url,
            "en": url,
        }
        self.location = location
        self.lunch_hours = lunch_hours
        self.lunch_price = lunch_price
        self.menu_fallback = {
            "fi": ["Tämän päivän lounasta ei löytynyt."],
            "en": ["Today's lunch menu not found."],
        }
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
                self.menu = self.parse_menu(soup, lang)
            elif format == "pdf":
                if self.url:
                    pdf_content = await self.fetch_pdf_content(self.url)
                    text = self.extract_text_from_pdf(pdf_content)
                    self.menu = self.parse_pdf_menu(text, lang)
                else:
                    self.menu = self.menu_fallback[lang]
            elif format == "json":
                content = await self.fetch_json_content(lang)
                self.menu = self.parse_json_menu(content, lang)
            else:
                raise ValueError("Unsupported format.")
            return (
                self.discount[lang],
                self.is_student_cantine,
                self.location,
                self.lunch_hours,
                self.lunch_price,
                self.menu,
                self.name,
                self.url,
            )
        except Exception:
            return (
                self.discount[lang],
                self.is_student_cantine,
                self.location,
                self.lunch_hours,
                self.lunch_price,
                self.menu_fallback[lang],
                self.name,
                self.url,
            )
