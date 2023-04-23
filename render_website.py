import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')

    with open(os.path.join('media', 'books', 'books.json'), 'r', encoding='utf-8') as file:
        books = json.load(file)
        books_quantity = len(books)
        books_per_page = 10
        pages_quantity = math.ceil(books_quantity / books_per_page)

        books_on_page = []
        page_number = 0

        for index, book in enumerate(books, start=1):
            books_on_page.append(book)
            if index % books_per_page == 0 or index == len(books):
                chunked_books_on_page = chunked(books_on_page, 2)
                rendered_page = template.render(
                    books=chunked_books_on_page,
                    current_page_number=page_number + 1,
                    pages_quantity=pages_quantity
                )

                if page_number != 0:
                    page_name = f'index{page_number + 1}.html'
                else:
                    page_name = 'index.html'

                books_on_page = []
                page_number += 1

                with open(os.path.join('pages', page_name), 'w', encoding="utf8") as file:
                    file.write(rendered_page)


if __name__ == '__main__':
    os.makedirs('pages', exist_ok=True)
    os.makedirs('media/images', exist_ok=True)

    main()

    server = Server()
    server.watch('render_website.py', main)
    server.watch('template.html', main)

    server.serve(root='.')
