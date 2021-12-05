import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def title_book(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_spec = soup.find('body').find('h1').text
    return (book_spec.strip().split('::')[0].strip(),
            book_spec.strip().split('::')[1].strip())


def get_img_url(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    anchor = soup.find(class_='bookimage').find('img')['src']
    return urljoin(url, anchor)


def download_img(img_folder, img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    img_name = urlparse(img_url).path.split('/')[-1]
    filepath = os.path.join(img_folder, img_name)
    with open(f'{filepath}', 'wb') as file:
        file.write(response.content)


def download_txt(title, folder, id):
    url = 'https://tululu.org/txt.php'
    payload = {'id': id}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_redirect(response.history)
    filepath = os.path.join(folder, f'{id}.{sanitize_filename(title)}.txt')
    with open(f'{filepath}', 'w') as file:
        file.write(response.text)
    return filepath


def download_comments(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all(class_='texts')
    for comment in comments:
        print(comment.text.split(')')[-1])


def check_redirect(response):
    if response:
        raise requests.HTTPError('Redirect to main')


folder = 'books'
img_folder = 'images'
os.makedirs(img_folder, exist_ok=True)
os.makedirs(folder, exist_ok=True)


for id in range(5, 11):
    try:
        title, author = title_book(id)
        download_txt(title, folder, id)
        img_url = get_img_url(id)
        download_img(img_folder, img_url)
        # download_comments(id)
    except:
        continue


