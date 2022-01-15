import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked, chunked_even


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open('results/books.json', 'r') as file:
    books_json = file.read()

content = list(chunked_even(list(chunked(json.loads(books_json), 2)), 10))

def on_reload(content):
    template = env.get_template('template.html')
    for num, page in enumerate(content, 1):
        rendered_page = template.render(books=page)
        with open(f'pages/index{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

on_reload(content)

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')



# def on_reload(books):
#     template = env.get_template('template.html')
#     rendered_page = template.render(books=list(chunked(books, 2)))
#     with open('index.html', 'w', encoding="utf8") as file:
#         file.write(rendered_page)

