import argparse
import os
import pprint
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_book_spec(html_page):
    book_spec = html_page.find('body').find('h1').text
    return (book_spec.strip().split('::')[0].strip(),
            book_spec.strip().split('::')[1].strip())


def get_genre(html_page):
    genre = html_page.find('span', class_='d_book')
    return genre.text.split(':')[-1].replace('.', '').strip()


def get_comments(html_page):
    user_comments = html_page.find_all(class_='texts')
    comments = []
    for comment in user_comments:
        comments.append(comment.text.split(')')[-1])
    return comments


def get_img_url(book_id):
    url = f'https://tululu.org/b{book_id}/'
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


def download_txt(title, folder, book_id):
    url = 'https://tululu.org/txt.php'
    payload = {'id': book_id}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_redirect(response.history)
    filepath = os.path.join(folder, f'{book_id}.{sanitize_filename(title)}.txt')
    with open(f'{filepath}', 'w') as file:
        file.write(response.text)
    return filepath


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    check_redirect(response.history)
    html_page = BeautifulSoup(response.text, 'lxml')
    title, author = get_book_spec(html_page)
    genre = get_genre(html_page)
    comments = get_comments(html_page)
    book_description = {
        'id': book_id,
        'Автор': author,
        'Название': title,
        'Жанр': genre,
        'Отзывы': comments
    }
    return title, book_description


def check_redirect(response):
    if response:
        raise requests.HTTPError('Redirect to main')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт парсит данные сайта tululu.org'
                    'скачивает книги и показывает её данные'
    )

    parser.add_argument(
        '--start_id',
        type=int,
        default=1,
        help='Укажите start_id'
    )

    parser.add_argument(
        '--end_id',
        type=int,
        default=10,
        help='Укажите end_id'
    )

    args = parser.parse_args()

    folder, img_folder = 'books', 'images'
    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(folder, exist_ok=True)

    for book_id in range(args.start_id, args.end_id):
        try:
            title, book_description = parse_book_page(book_id)
            download_txt(title, folder, book_id)
            img_url = get_img_url(book_id)
            download_img(img_folder, img_url)
            pprint.pprint(book_description)
        except:
            continue
