import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def title_book(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_spec = soup.find('body').find('h1').text
    return (book_spec.strip().split('::')[0].strip(),
            book_spec.strip().split('::')[1].strip())


def check_redirect(response):
    if response:
        raise requests.HTTPError('Redirect to main')


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


folder = 'books/'
os.makedirs(folder, exist_ok=True)
for id in range(1, 11):
    try:
        title, author = title_book(id)
        filepath = download_txt(title, folder, id)
        print(filepath)
    except:
        continue


