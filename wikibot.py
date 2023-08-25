import requests
from bs4 import BeautifulSoup

def get_intro_paragraph(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        result = ""

        mw_parser_output = soup.find('div', class_='mw-parser-output')
        if mw_parser_output:
            paragraphs = mw_parser_output.find_all('p')
            for paragraph in paragraphs:
                if paragraph.text.strip() and len(result) < 500:  # Ignore empty paragraphs
                    result += paragraph.get_text()
        return result
    else:
        return "Page not found."

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Special:Random"
    intro_paragraph = get_intro_paragraph(url)
    print(intro_paragraph)
