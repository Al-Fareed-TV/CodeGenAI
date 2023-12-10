import requests
from bs4 import BeautifulSoup

def save_html(url, output_file="output.html"):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for script in soup(["script", "style"]):
                script.extract()
        
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
                
            print(f"HTML content saved to {output_file}")

        else:
            print(f"Failed to retrieve HTML. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url_to_scrape = "https://rahulshettyacademy.com/loginpagePractise/"
save_html(url_to_scrape, output_file="output.html")
