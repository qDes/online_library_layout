import json

from livereload import Server
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_books_description(filename):
    with open(filename, 'r') as f:
        description = json.loads(f.read())
    return description


def make_books_chunks(books, chunk_size=25):
    chunks = [books[x:x+chunk_size] for x in range(0, len(books), chunk_size)]
    return chunks


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books = get_books_description('description.json')
    books_chunks = make_books_chunks(books)
    for num, chunk in enumerate(books_chunks):
        rendered_page = template.render(books=chunk)
        with open(f'pages/index{num+1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    server = Server()
    server.watch('template.html', on_reload)
    server.watch('render_website.py', on_reload)
    server.serve(root='.')
    #server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    #server.serve_forever()
