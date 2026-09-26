from scrapers.base import RestaurantScraper
import datetime
import re
import httpx
from bs4 import BeautifulSoup

# Restaurant is closed Monday, Saturday and Sunday (weekday(): Mon=0 ... Sun=6)
CLOSED_WEEKDAYS = {0, 5, 6}


class DaSpizzicoScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Da Spizzico",
            "https://foodzone.fi/helsinki/daspizzico/lunch",
            "https://maps.app.goo.gl/FfAnM3uzkffkgTzWA",
            "12 - 14€",
            "11:00 - 14:30",
        )
        self.lang_urls = {
            "fi": "https://foodzone.fi/helsinki/daspizzico/lunch",
            "en": "https://foodzone.fi/helsinki/daspizzico/lunch",
        }
        self.api_url = "https://foozu3.fi/website_common_code/views/buffet/buffet-design-1.php"
        self.region = "jatkasaari"

    def parse_menu(self, soup, lang):
        """
        Fetch and parse today's lunch menu
        This method fetches the menu from the API and parses it
        """
        if datetime.date.today().weekday() in CLOSED_WEEKDAYS:
            return self.menu_fallback.get(lang, [])

        # Map language codes
        lang_code_map = {"fi": "FI", "en": "EN"}
        lang_id_map = {"fi": "2", "en": "1"}

        lang_code = lang_code_map.get(lang, "FI")
        lang_id = lang_id_map.get(lang, "2")

        # Headers matching the curl request
        # Note: We remove Accept-Encoding to let httpx handle compression automatically
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,sv-FI;q=0.8,fr-FR;q=0.7,fi;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://foodzone.fi",
            "Connection": "keep-alive",
            "Referer": "https://foodzone.fi/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }

        # POST data matching the curl request
        data = {
            "required_variables[web_common_url]": "https://foozu3.fi/website_common_code/",
            "required_variables[website_url]": "https://foodzone.fi/",
            "required_variables[lang_code]": lang_code,
            "required_variables[lang_id]": lang_id,
            "required_variables[loc_id]": "38",  # Da Spizzico location ID
            "required_variables[page_id]": "3",  # buffet/lunch page
            "required_variables[user_id]": "0",
            "required_variables[view_from]": "website",
            "required_variables[selqrcodedeliverytypeid]": "0",
            "required_variables[qr_code_id]": "0",
            "required_variable_data_input_echo": "1",
            "sesstion_order_id": "0",
            "payment_success_fail_status": "0",
            "payment_authcode": "0",
            "url_city": "helsinki",
            "stripe_checkout_session_id": "",
        }

        try:
            # Use httpx with sync client
            with httpx.Client(timeout=10.0) as client:
                response = client.post(self.api_url, headers=headers, data=data)

            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                return self.menu_fallback.get(lang, [])

            # httpx automatically handles decompression
            html = response.text

        except Exception as e:
            print(f"Error fetching menu: {e}")
            return self.menu_fallback.get(lang, [])

        # Parse the HTML response
        soup = BeautifulSoup(html, "html.parser")
        menu_items = []

        # Find the menu container
        menu_div = soup.find("div", class_=re.compile(r"col-12|col-md-6"))

        if not menu_div:
            # Try to find any div with menu content
            menu_div = soup

        # Extract all paragraph elements
        paragraphs = menu_div.find_all("p")

        current_dish = None
        # True once the current dish has received a description line (lowercase text).
        # A dish name and its price are sometimes split across separate <br> lines
        # (e.g. "LASAGNA BOLOGNESE" then "13" on the next line), so consecutive
        # header fragments (no lowercase letters) must be merged together rather
        # than being mistaken for a new item or a description.
        dish_complete = False

        for p in paragraphs:
            # Get text with original formatting preserved
            text = p.get_text(separator="\n", strip=True)

            # Skip empty, headers, and unwanted text
            if not text or text == "&nbsp;":
                continue
            if any(
                skip in text
                for skip in [
                    "Lounas",
                    "TI-Pe",
                    "Vk.",
                    "Lämpimästi tervetuoloa",
                    "Salaatti, Itseleivottu leipä",
                    "sisältää lounaaseen",
                    "gluteeniton",
                ]
            ):
                continue

            # Split by newlines to handle multi-line paragraphs
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            for line in lines:
                # Clean up whitespace
                line = re.sub(r"\s+", " ", line)

                # Remove leading dashes
                line = line.lstrip("-").strip()

                # Skip if too short
                if len(line) < 2:
                    continue

                is_description = any(c.islower() for c in line)

                if is_description:
                    # Description lines (ingredients) are always lowercase
                    if current_dish:
                        current_dish = f"{current_dish}: {line}"
                    else:
                        current_dish = line
                    dish_complete = True
                else:
                    # Header fragment: a dish name and/or its price, with no lowercase text
                    if current_dish is None or dish_complete:
                        if current_dish:
                            menu_items.append(current_dish)
                        current_dish = line
                        dish_complete = False
                    else:
                        # Still building the header (e.g. name and price on separate lines)
                        current_dish = f"{current_dish} {line}"

        # Don't forget the last dish
        if current_dish:
            menu_items.append(current_dish)

        # If no items found, try alternative parsing with strong tags
        if not menu_items:
            strong_tags = menu_div.find_all("strong")
            for strong in strong_tags:
                text = strong.get_text(strip=True)
                text = re.sub(r"\s+", " ", text)
                text = text.lstrip("-").strip()

                if (
                    text
                    and "€" in text
                    and not any(skip in text for skip in ["TI-Pe", "gluteeniton", "Lounas"])
                ):
                    menu_items.append(text)

        return menu_items if menu_items else self.menu_fallback.get(lang, [])
