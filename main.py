import requests
import os

path = 'books/'
os.makedirs(path, exist_ok=True)

url = 'https://tululu.org/txt.php'

for id in range(1, 11):
    payload = {
        'id': id
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(f'{path}book{id}.txt', 'w') as file:
        file.write(response.text)
