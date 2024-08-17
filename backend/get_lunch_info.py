import requests

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}



def get_bruuveri_lunch_info():

    url = "https://www.bruuveri.fi/lounas-menu/"
    lunch_price = "13,50€ (Noutopöytä), 12,30€ (Kevytlounas)"
    lunch_available = "11:00 - 14:00"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get current day and month
        specific_date = datetime.now() + timedelta(days=3)
        target_day = specific_date.day 
        target_month = specific_date.month
        target_date_str = f"{target_day}.{target_month}."

        # Find the menu for the specific date
        menu_items = []
        for menu in soup.find_all('div', class_='heading-text'):
            text = menu.get_text(strip=True)
            # Check if the text contains the target date
            if target_date_str in text:
                # Get the next sibling containing the menu items
                next_sibling = menu.find_next('div', class_='vc_custom_heading_wrap')
                while next_sibling:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    if any(char.isdigit() for char in menu_text):
                        break
                    menu_items.append(menu_text)
                    next_sibling = next_sibling.find_next('div', class_='vc_custom_heading_wrap')
                break

        if menu_items:
            menu = "\n".join(menu_items)

        else:
            menu = f"Lounasta ei saatavilla {target_date_str}"
        
        return menu, lunch_price, lunch_available

    except Exception as e:
        return f"Virhe: {str(e)}"
    
def get_kansis_lunch_info():
    
    url = "https://ravintolakansis.fi/lounas/"
    lunch_price = "12.70 - 14.20€"
    lunch_available = "11:00 - 14:00"
    menu = "Menu not defined for Kansis"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get current day and month
        specific_date = datetime.now() - timedelta(days=3)
        target_day = specific_date.day 
        target_month = specific_date.month
        target_date_str = f"{target_day}.{target_month}"

        menu = html_content

        # Find the menu for the specific date
        menu_items = []
        for heading in soup.find_all('h3'):
            text = heading.get_text(strip=True)
            # Check if the text contains the target date
            if target_date_str in text:
                # Find the parent container that holds the h3 and its relevant siblings
                parent_div = heading.find_parent()
                next_sibling = heading.find_next_sibling()
                while next_sibling and next_sibling in parent_div:
                    menu_text = next_sibling.get_text(separator="\n", strip=True)
                    menu_items.append(menu_text)
                    next_sibling = next_sibling.find_next_sibling()
                break

        if menu_items:
            menu = "\n".join(menu_items)

        else:
            menu = f"Lounasta ei saatavilla {target_date_str}"
    
        return menu, lunch_price, lunch_available
    
    except Exception as e:
        return f"Virhe: {str(e)}"


def get_plaza_lunch_info():
    
    url = "https://www.ardenrestaurants.fi/menut/plazatabletmenu.html"
    lunch_price = "14.50€"
    lunch_available = "10:30 - 14:00"
    menu = "Menu not defined for Plaza"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get current day and month
        specific_date = datetime.now()
        target_day = specific_date.day
        target_month = specific_date.month
        target_date_str = f"{target_day}.{target_month}."

        # Muokkaa
        menu = "Ruokalista"

        return menu, lunch_price, lunch_available

    except Exception as e:
        return f"Virhe: {str(e)}"

def get_quem_lunch_info():
    pass

def get_pompier_albertinkatu_info():
    pass

def get_lunch_info(restaurant_name):
    if restaurant_name == "bruuveri":
        return get_bruuveri_lunch_info()
    
    elif restaurant_name == "kansis":
        return get_kansis_lunch_info()
    
    else:
        return get_bruuveri_lunch_info()