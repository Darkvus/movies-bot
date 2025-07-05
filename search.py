# search_mejortorrent.py
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www30.mejortorrent.eu"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_mejortorrent(query):
    query = query.lower()
    response = requests.get(f"{BASE_URL}/busqueda?q={query}", headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching search results: {response.status_code}")
        print(response.text)
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    print(f"Found {len(links)} links in the search results.")
    print(f"Links: {links}")
    for link in links:
        href = link.get("href")
        if href and re.match(r"^https://www\d+\.mejortorrent\.eu/pelicula/\d+/", href):
            print(href)
            return get_torrent_url(href)
    return None

def get_torrent_url(detail_url):
    response = requests.get(detail_url, headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    torrent_link = soup.find("a", href=lambda href: href and href.endswith(".torrent"))
    print(f" Torrent url is: {BASE_URL}{torrent_link['href']}")
    return f"{BASE_URL}{torrent_link['href']}" if torrent_link else None
