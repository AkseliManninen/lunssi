import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Bruuveri
url = "https://www.bruuveri.fi/lounas-menu/"

def get_bruuveri_menu():
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
            return "\n".join(menu_items)
        else:
            return f"No menu found for {target_date_str}."
    except Exception as e:
        return f"Failed to retrieve the menu. Error: {str(e)}"
    
def get_kansis_menu():
    pass

def get_plaza_menu():
    pass

def get_menu(restaurant_name):
    if restaurant_name == "bruuveri":
        return get_bruuveri_menu()
    else:
        return "No menu yet for kansis"

if __name__ == "__main__":
    menu = get_menu("bruuveri")
    print(menu)
