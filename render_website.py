import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked, chunked_even


def on_reload(content, template):
    for num, page in enumerate(content, 1):
        rendered_page = template.render(books=page, pages=len(content) + 1)
        with open(f'pages/index{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open('results/books.json', 'r') as file:
        books_json = file.read()

    template = env.get_template('template.html')
    content = list(chunked_even(list(chunked(json.loads(books_json), 2)), 10))

    on_reload(content, template)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
