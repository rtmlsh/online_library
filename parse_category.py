from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_book_urls(page_id):
    url = f'https://tululu.org/l55/{page_id}/'
    response = requests.get(url)
    response.raise_for_status()
    html_page = BeautifulSoup(response.text, 'lxml')
    anchors = html_page.find_all(class_='d_book')
    book_urls = [urljoin(url, anchor.find('a')['href']) for anchor in anchors]
    return book_urls
