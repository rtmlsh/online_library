import argparse
import json
import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from check_redirect import check_redirect
from parse_category import parse_book_urls


def get_last_page():
    url = f'https://tululu.org/l55/1/'
    response = requests.get(url)
    response.raise_for_status()
    check_redirect(response.history)
    html_page = BeautifulSoup(response.text, 'lxml')
    last_page = int(html_page.select_one('.npage:last-child').text) + 1
    return last_page


def download_img(img_folder, img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    img_name = urlparse(img_url).path.split('/')[-1]
    filepath = os.path.join(img_folder, img_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_txt(title, folder, url):
    book_id = urlparse(url).path.strip('/').split('b')[-1]
    download_url = 'https://tululu.org/txt.php'
    payload = {'id': book_id}
    response = requests.get(download_url, params=payload)
    response.raise_for_status()
    check_redirect(response.history)
    filepath = os.path.join(folder, f'{sanitize_filename(title)}.txt')
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath


def get_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    check_redirect(response.history)
    html_page = BeautifulSoup(response.text, 'lxml')
    return html_page


def parse_book_page(html_page, url, folder, img_folder):
    book_spec = html_page.select_one('body h1').text
    title, author = book_spec.strip().split('::')
    genre = html_page.select_one('span.d_book').text
    book_genre = genre.split(':')[-1].replace('.', '').strip()
    anchor = html_page.select_one('.bookimage img')['src']
    user_comments = html_page.select('.texts')
    comments = [comment.text.split(')')[-1] for comment in user_comments]
    book_description = {
        'author': author.strip(),
        'title': title.strip(),
        'genre': book_genre,
        'reviews': comments,
        'img_url': urljoin(url, anchor),
        'img_src': f'{img_folder}/{anchor.split("/")[-1]}',
        'book_path': f'{folder}/{title.strip()}.txt'
    }
    return book_description


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт парсит данные сайта tululu.org'
                    'скачивает книги и показывает её данные'
    )

    parser.add_argument(
        '--start_page',
        type=int,
        default=1,
        help='Укажите start_page'
    )

    parser.add_argument(
        '--last_page',
        type=int,
        default=get_last_page(),
        help='Укажите last_page'
    )

    parser.add_argument(
        '--dest_folder',
        default='results',
        help='Укажите каталог для сохранения результатов',
    )

    parser.add_argument(
        '--json_path',
        default='results',
        help='Укажите каталог для сохранения json'
    )

    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Булево значение true, если картинки не нужны'
    )

    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Булево значение true, если txt не нужны'
    )

    args = parser.parse_args()

    folder = f'{args.dest_folder}/books'
    img_folder = f'{args.dest_folder}/images'
    json_folder = args.json_path
    os.makedirs(folder, exist_ok=True)
    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    book_descriptions = []
    for page_num in range(args.start_page, args.last_page):
        try:
            book_urls = parse_book_urls(page_num)
            for url in book_urls:
                html_page = get_book_page(url)
                book_description = parse_book_page(
                    html_page,
                    url,
                    folder,
                    img_folder
                )
                if not args.skip_txt:
                    download_txt(
                        book_description['title'],
                        folder,
                        url,
                    )
                if not args.skip_imgs:
                    download_img(
                        img_folder,
                        book_description['img_url']
                    )
                book_descriptions.append(book_description)
                print(url)
        except requests.HTTPError:
            continue

    with open(f'{json_folder}/books.json', 'w') as file:
        json.dump(book_descriptions, file, ensure_ascii=False)
