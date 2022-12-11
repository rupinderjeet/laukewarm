import re

from bs4 import BeautifulSoup


class BookListHtmlReader:

    def __init__(self, file_path):
        self.__input_file_path = file_path

    def get_books(self):
        with open(self.__input_file_path) as file:
            content = file.read()

        document = BeautifulSoup(content, "html.parser")
        return self.__parse(document)

    def __parse(self, document):
        # -> <td width='233' valign='middle' height='200'>
        elements = document.find_all('td', attrs={'width': '233', 'valign': 'middle', 'height': '200'})
        books = []
        for element in elements:
            book = {
                'author_name': self.__read_author_name(element),
                'id': self.__read_id(element),
                'name': self.__read_name(element),
                'page_count': self.__read_page_count(element),
                'publisher': self.__read_publisher(element),
                'publish_year': self.__read_publish_year(element),
                'rating': self.__read_rating(element),
                'script': self.__read_script(element),
                'thumbnail': self.__read_thumbnail(element),
            }
            self.__verify_book_missing_info(element)
            books.append(book)

        return books

    @staticmethod
    def __read_author_name(element):
        # -> a href='#' title='Author'
        anchor = element.find('a', attrs={'href': '#', 'title': 'Author'})
        if anchor:
            return anchor.string.strip()

    @staticmethod
    def __read_id(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a class='leftList' href
        #      -> search text 'ID=\d+'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchor = td.find('a', class_='leftList')
            if anchor:
                text = anchor.attrs['href'].strip()
                if 'ID=' in text:
                    matches = re.findall(r'ID=\d+', text)
                    for match in matches:
                        count = match.replace('ID=', '').strip()
                        if count.isdigit():
                            return int(count)

    @staticmethod
    def __read_name(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a class='leftList'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchor = td.find('a', class_='leftList')
            if anchor:
                return anchor.string.strip()

    @staticmethod
    def __read_page_count(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> search text '\d+ pages'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            text = td.text
            if 'pages' in text:
                matches = re.findall(r'\d+ pages', text)
                for match in matches:
                    count = match.replace('pages', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_publisher(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a href='#' title='Publisher'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchor = td.find('a', attrs={'href': '#', 'title': 'Publisher'})
            if anchor:
                return anchor.string.strip()

    @staticmethod
    def __read_publish_year(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a href='#' title='PublisherYear'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchor = td.find('a', attrs={'href': '#', 'title': 'PublisherYear'})
            if anchor:
                return anchor.string.strip()

    @staticmethod
    def __read_rating(element):
        # -> search 'img' tags with 'name' & 'src' (must end in 'withoutRating.gif')
        img_list = element.find_all('img')
        return sum(img.has_attr('name')
                   and img.has_attr('src')
                   and img.attrs['src'].endswith('withoutRating.gif')
                   for img in img_list)

    @staticmethod
    def __read_script(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a href='#' title='Script'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchor = td.find('a', attrs={'href': '#', 'title': 'Script'})
            if anchor:
                return anchor.string.strip()

    @staticmethod
    def __read_thumbnail(element):
        # -> <td height='95' valign='middle' align='center'>
        #   -> a
        #     -> img
        td_list = element.find_all('td', attrs={'height': '95', 'valign': 'middle', 'align': 'center'})
        for td in td_list:
            img = td.find('a').find('img')
            if img:
                # TODO: verify thumbnail url integrity
                # TODO: use absolute thumbnail urls
                return img.attrs['src']

    @staticmethod
    def __verify_book_missing_info(element):
        # -> <td width='100%' colspan='2' height='25'>
        #   -> a href='#'
        #       -> not 'title' contains 'Author|Publisher|PublisherYear|Script'
        td_list = element.find_all('td', attrs={'width': '100%', 'colspan': '2', 'height': '25'})
        for td in td_list:
            anchors = td.find_all('a', attrs={'href': '#'})
            for anchor in anchors:
                if anchor.attrs['title'] in 'Author|Publisher|PublisherYear|Script':
                    continue
                print(f'missing-info: {anchor}')
