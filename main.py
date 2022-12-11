import json

from reader.book_detail_html_reader import BookDetailHtmlReader
from reader.book_list_html_reader import BookListHtmlReader


def load_book_list():
    reader = BookListHtmlReader('sample/books.html')
    print(json.dumps(reader.get_books(), indent=2))


def load_book_detail():
    reader = BookDetailHtmlReader('sample/bookdetail.html')
    print(json.dumps(reader.get_book_detail(), indent=2))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # load_book_list()
    load_book_detail()
    # download_book_list_pages()
    print('__done__')
