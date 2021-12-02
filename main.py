import requests
import os

path = 'books/'
os.makedirs(path, exist_ok=True)


def downoload_books(path, id):
    url = 'https://tululu.org/txt.php'
    payload = {'id': id}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_redirect(response.history)
    with open(f'{path}book{id}.txt', 'w') as file:
        file.write(response.text)
    return response.history


def check_redirect(response):
    if response:
        raise requests.HTTPError('Redirect to main')


for id in range(1, 11):
    try:
        response = downoload_books(path, id)
    except:
        continue


