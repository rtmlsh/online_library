import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pprint


url = 'https://tululu.org/l55/'
response = requests.get(url)
response.raise_for_status()
html_page = BeautifulSoup(response.text, 'lxml')
anchors = html_page.find_all(class_='d_book')
book_urls = [urljoin(url, anchor.find('a')['href']) for anchor in anchors]
pprint.pprint(book_urls)


