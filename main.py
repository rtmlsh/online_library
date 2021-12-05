import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pprint


def title_book(url):
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


def get_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    user_comments = soup.find_all(class_='texts')
    comments = []
    for comment in user_comments:
        comments.append(comment.text.split(')')[-1])
    return comments


def get_genre(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    genre = soup.find('span', class_='d_book')
    return genre.text.split(':')[-1].replace('.', '').strip()


def parse_book_page(id):
    url = f'https://tululu.org/b{id}/'
    title, author = title_book(url)
    genre = get_genre(url)
    comments = get_comments(url)
    book_description = {
        'Автор': author,
        'Название': title,
        'Жанр': genre,
        'Отзывы': comments
    }
    return title, book_description


def check_redirect(response):
    if response:
        raise requests.HTTPError('Redirect to main')


folder = 'books'
img_folder = 'images'
os.makedirs(img_folder, exist_ok=True)
os.makedirs(folder, exist_ok=True)


for id in range(5, 11):
    try:
        title, book_description = parse_book_page(id)
        download_txt(title, folder, id)
        img_url = get_img_url(id)
        download_img(img_folder, img_url)
        pprint.pprint(book_description)
    except:
        continue


