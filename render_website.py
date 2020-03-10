import json

from livereload import Server
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_books_description(filename):
    with open(filename, 'r') as f:
        description = json.loads(f.read())
    return description


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books = get_books_description('description.json')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
    #server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    #server.serve_forever()
