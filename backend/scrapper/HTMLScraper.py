import requests
from bs4 import BeautifulSoup

class HTMLScraper:
    def __init__(self):
        self.headers = None

    def remove_css_js_and_save_html(self, url):
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for script in soup(["script", "style"]):
                    script.extract()

                return soup.prettify()

            else:
                print(f"Failed to retrieve HTML. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")