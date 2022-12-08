import math
import os
import re
from mimetypes import guess_extension

import requests
from bs4 import BeautifulSoup

from config import configuration


def download_book_list_pages():
    url = configuration.api_base_url() + configuration.api_books_list_endpoint()

    # send an initial test request to determine total books
    total_books = __find_total_books(url, page_number=1, per_page=20)
    print(f'download_book_list_pages total books found: {total_books}')
    if not total_books:
        return

    # determine total pages to be fetched
    page_number = 1
    per_page = configuration.param_books_per_page()
    total_pages = math.ceil(total_books / per_page)

    # fetch all available pages
    while page_number <= total_pages:
        print(f'download_book_list_pages retrieving page:{page_number} per_page:{per_page}')
        response = __fetch_book_list_page(url=url, page_number=page_number, per_page=per_page)
        if response.status_code != 200:
            print(f'\tdownload_book_list_pages network required failed ({response.status_code})')
            continue
        __save_book_list_response(response, title=f'book-list-page-{page_number}')
        page_number += 1


def __find_total_books(url, page_number, per_page):
    __validate_page_number(page_number)
    __validate_per_page(per_page)

    response = __fetch_book_list_page(url=url, page_number=page_number, per_page=per_page)
    if response.status_code != 200:
        print(f'__find_total_books network request failed ({response.status_code})')
        return

    document = BeautifulSoup(response.content, "html.parser")

    pattern = re.compile(r'(\d+) to (\d+) of about (\d+) records')
    text = document.find(string=pattern)
    if not text:
        print(f'__find_total_books pattern-matching failed')
        return

    matches = pattern.search(text)
    from_index = matches.group(1)
    assert int(from_index) == ((page_number * per_page) - per_page) + 1

    to_index = matches.group(2)
    assert int(to_index) == page_number * per_page

    total = matches.group(3)
    return int(total)


def __fetch_book_list_page(url, page_number, per_page):
    __validate_page_number(page_number)
    __validate_per_page(per_page)

    headers = {'Content-Type': 'application/x-www-form-urlencoded', }
    params = {'CategoryID': 1, 'viewall': 1, 'page': page_number, }
    data = f'rpp={per_page}'

    return requests.post(url, headers=headers, params=params, data=data)


def __save_book_list_response(response, title):
    mime_type = response.headers['content-type'].partition(';')[0].strip()
    extension = guess_extension(mime_type)
    file_name = title + extension

    output_directory_path = configuration.param_output_directory_path()
    output_directory_path = os.path.expanduser(output_directory_path)
    output_directory_path = os.path.join(output_directory_path, configuration.param_temp_folder_path())
    os.makedirs(output_directory_path, exist_ok=True)

    file_path = os.path.join(output_directory_path, file_name)

    with open(file_path, 'wb') as file:
        file.write(response.content)


def __validate_page_number(page_number):
    """Ensures input is valid

    :param page_number: int in (1 <= n <= 1000)
    :return: None
    """
    assert isinstance(page_number, int)
    assert page_number in range(1, 1000 + 1)


def __validate_per_page(per_page):
    """Ensures input is valid

    :param per_page: int in (20 <= n <= 100)
    :return: None
    """
    assert isinstance(per_page, int)
    assert per_page in range(20, 100 + 1)
