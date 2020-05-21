import glob
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def delete_old_files(directory):
    files_to_delete = glob.glob(f"{directory}/*")
    for file_ in files_to_delete:
        os.remove(file_)


def get_books_description(filename):
    with open(filename, 'r') as f:
        description = json.loads(f.read())
    return description


def rebuild_pages():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books = get_books_description('description.json')
    books_chunks = list(chunked(books, 25))
    delete_old_files(directory="pages")
    for num, chunk in enumerate(books_chunks, 1):
        rendered_page = template.render(books=chunk,
                                        num_pages=len(books_chunks),
                                        current_page=num)
        with open(f'pages/index{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    rebuild_pages()
    server = Server()
    server.watch('template.html', rebuild_pages)
    server.watch('render_website.py', rebuild_pages)
    server.serve(root='.')
