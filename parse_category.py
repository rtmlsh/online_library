from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_redirect import check_redirect


def parse_book_urls(page_num):
    url = f'https://tululu.org/l55/{page_num}/'
    response = requests.get(url)
    response.raise_for_status()
    check_redirect(response.history)
    html_page = BeautifulSoup(response.text, 'lxml')
    anchors = html_page.find_all(class_='d_book')
    book_urls = [urljoin(url, anchor.find('a')['href']) for anchor in anchors]
    return book_urls
