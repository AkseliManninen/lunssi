import pymupdf
import re

from bs4 import BeautifulSoup
from scrapers.base import RestaurantScraper


class MeilinScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Mei Lin",
            "https://www.meilin-fi.com/",
            "https://maps.app.goo.gl/mPLJQakzHAwo8aK28",
            "13,70€",
            "11:00 - 14:30",
        )

    async def get_pdf_url(self):
        content = await self.fetch_html_content(lang="fi")
        soup = BeautifulSoup(content, "html.parser")

        # The PDF filename changes when the menu is updated, so find it by link text.
        for link in soup.find_all("a", href=re.compile(r"\.pdf$")):
            if "lunch" in link.get_text().lower():
                return link["href"]
        return None

    def extract_text_from_pdf(self, pdf_content):
        # Each dish is "<Chinese> <Finnish> <English>", where the Finnish name is
        # bold and the English one is not. Use the font weight to put a " / "
        # between the two languages.
        doc = pymupdf.Document(stream=pdf_content)
        text = ""
        seen_finnish = False
        in_english = False
        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        span_text = span["text"]
                        is_bold = "Bold" in span["font"]
                        if re.match(r"^\d+\.", span_text.strip()):
                            seen_finnish = False
                            in_english = False
                        elif not span_text.strip() or re.search(r"[一-鿿]", span_text):
                            pass
                        elif is_bold and not in_english:
                            seen_finnish = True
                        elif not is_bold and seen_finnish and not in_english:
                            in_english = True
                            span_text = " / " + span_text
                        text += span_text
                    text += "\n"
        return text

    def parse_pdf_menu(self, text, lang):
        # The menu is the same every weekday: numbered dishes grouped under
        # section headings such as "2、 Vegan (100%) Lunch Menu".
        lunch_items = []
        current_lines = []
        for line in text.split("\n"):
            line = " ".join(line.split())
            if re.match(r"^\d+\.", line):
                if current_lines:
                    lunch_items.append(" ".join(current_lines))
                current_lines = [line]
            elif "、" in line:
                if current_lines:
                    lunch_items.append(" ".join(current_lines))
                current_lines = []
            elif line and current_lines:
                current_lines.append(line)
        if current_lines:
            lunch_items.append(" ".join(current_lines))

        lunch_items = [self.localize_item(item, lang) for item in lunch_items]
        return lunch_items if lunch_items else self.menu_fallback[lang]

    def localize_item(self, item, lang):
        # "1. 宫保鸡丁 Gong Pao Kanaa / Gong Pao Chicken" -> "1. Gong Pao Kanaa" (fi)
        # or "1. Gong Pao Chicken" (en). Items without a separator are kept whole.
        item = " ".join(re.sub(r"[一-鿿]+", " ", item).split())
        number, name = re.match(r"^(\d+\.)\s*(.*)$", item).groups()
        names = name.split(" / ", 1)
        name = names[1] if lang == "en" and len(names) == 2 else names[0]
        return f"{number} {name}"

    async def get_lunch_info(self, lang="fi", format="pdf"):
        self.url = await self.get_pdf_url()
        return await super().get_lunch_info(lang, format)
