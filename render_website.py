import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked, chunked_even


def on_reload(content, template, columns):
    for num, page_content in enumerate(content, 1):
        books = list(chunked(page_content, columns))
        rendered_page = template.render(
            books=books,
            pages=len(content),
            page_num=num
        )
        with open(
                f'pages/{"index" if num == 1 else f"index{num}"}.html',
                'w',
                encoding="utf8"
        ) as file:
            file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    columns = 2
    book_limit = 10

    with open('media/books.json', 'r') as file:
        books = json.load(file)

    template = env.get_template('template.html')
    content = list(chunked_even(books, book_limit))

    on_reload(content, template, columns)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
