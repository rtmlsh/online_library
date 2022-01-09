import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open('results/books.json', 'r') as file:
    books_json = file.read()

books = list(chunked(json.loads(books_json), 2))

def on_reload(books):
    template = env.get_template('template.html')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

on_reload(books)

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
