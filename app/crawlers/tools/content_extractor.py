import requests
from bs4 import BeautifulSoup


def extract_webpage_content(url: str):

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join(p.get_text() for p in paragraphs[:15])

        return text[:2500]

    except Exception:
        return "Failed to extract webpage content."
