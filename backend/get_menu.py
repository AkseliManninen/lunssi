import requests

#from bs4 import BeautifulSoup

#def get_menu():
#    url = "https://www.bruuveri.fi/lounas-menu/"
#    response = requests.get(url)
    
#    if response.status_code == 200:
#        soup = BeautifulSoup(response.content, "html.parser")
#        menu_section = soup.find("div", {"class": "entry-content"})  # Adjust this selector based on actual HTML structure
        
#        if menu_section:
#            menu_items = menu_section.find_all("p")
#            menu = [item.get_text(strip=True) for item in menu_items]
#            return {
#                "name": "Bruuveri",
#                "lunchItems": menu,
#                "lunchPrice": 10.99,  # You can change this to the actual price if available
#                "lunchTime": "11:00 AM - 2:00 PM",  # Adjust to actual lunch time if available
#            }
#        else:
#            return {"error": "Menu section not found"}
#    else:
#        return {"error": f"Failed to retrieve the page. Status code: {response.status_code}"}

# TO-DO get the information
def get_menu():
    return 11

if __name__ == "__main__":
    menu = get_menu()
    print(menu)
