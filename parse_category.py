import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


url = 'https://tululu.org/l55/'
response = requests.get(url)
response.raise_for_status()
html_page = BeautifulSoup(response.text, 'lxml')
anchor = html_page.find(class_='d_book').find('a')['href']
print(urljoin(url, anchor))


