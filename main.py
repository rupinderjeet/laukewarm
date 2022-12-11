import json

from bs4 import BeautifulSoup

from book_detail import read_book
from reader.book_list_html_reader import BookListHtmlReader


def load_book_list():
    reader = BookListHtmlReader('sample/books.html')
    print(json.dumps(reader.get_books(), indent=2))


def load_book_detail():
    with open('sample/bookdetail.html') as file:
        content = file.read()

    document = BeautifulSoup(content, "html.parser")
    book = read_book(document)
    print(json.dumps(book, indent=2))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_book_list()
    # load_book_detail()
    # download_book_list_pages()
    print('__done__')
