import re

from bs4 import BeautifulSoup


class BookDetailHtmlReader:

    def __init__(self, file_path):
        self.__input_file_path = file_path

    def get_book_detail(self):
        with open(self.__input_file_path) as file:
            content = file.read()

        document = BeautifulSoup(content, "html.parser")
        return self.__parse(document)

    def __parse(self, document):
        left_pane = document.find('td', attrs={'width': '31%', 'valign': 'top', 'height': '300'})
        right_pane = document.find('td', attrs={'width': '69%', 'valign': 'top'})
        book = {
            'accession_code': self.__read_accession_code(right_pane),
            'author_name': self.__read_author_name(right_pane),
            'author_id': self.__read_author_id(right_pane),
            'completion': self.__read_completion_status(right_pane),
            'condition': self.__read_condition(right_pane),
            'custodian_name': self.__read_custodian_name(right_pane),
            'custodian_id': self.__read_custodian_id(right_pane),
            'download_count': self.__read_download_count(left_pane),
            'file_size': self.__read_file_size(left_pane),
            'file_url': self.__read_file_url(left_pane),
            'id': self.__read_id(left_pane),
            'language': self.__read_language(right_pane),
            'language_id': self.__read_language_id(right_pane),
            'name': self.__read_name(document),
            'page_breadth': self.__read_page_breadth(right_pane),
            'page_count': self.__read_page_count(right_pane),
            'page_length': self.__read_page_length(right_pane),
            'publisher': self.__read_publisher(right_pane),
            'publisher_id': self.__read_publisher_id(right_pane),
            'publish_year': self.__read_publish_year(right_pane),
            'rating': self.__read_rating(left_pane),
            'script': self.__read_script(right_pane),
            'script_id': self.__read_script_id(right_pane),
            'sponsor': self.__read_sponsor(right_pane),
            'sponsor_id': self.__read_sponsor_id(right_pane),
            'thumbnail': self.__read_thumbnail(left_pane),
        }
        self.verify_book_missing_info(document)
        return book

    @staticmethod
    def __read_accession_code(element):
        # -> next element after (td > font text='Accession Number')
        fonts = element.select('td > font')
        for font in fonts:
            if 'Accession Number' in font.text:
                return font.parent.text.replace('Accession Number', '').strip()

    @staticmethod
    def __read_author_id(element):
        # -> td > a [href='.....Author=ID.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            href = anchor.attrs['href']
            if 'Author=' in href:
                matches = re.findall(r'Author=\d+', href)
                for match in matches:
                    count = match.replace('Author=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_author_name(element):
        # -> td > a [href='.....Author=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Author=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_completion_status(element):
        # -> td > a [href='.....Completion=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Completion=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_condition(element):
        # -> td > a [href='.....DocCondition=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'DocCondition=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_custodian_id(element):
        # -> td > a [href='.....Contributor=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            href = anchor.attrs['href']
            if 'Contributor=' in href:
                matches = re.findall(r'Contributor=\d+', href)
                for match in matches:
                    count = match.replace('Contributor=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_custodian_name(element):
        # -> td > a [href='.....Contributor=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Contributor=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_download_count(element):
        # -> div id='downloadpdf'
        #   -> search text 'Downloaded \d+ times'
        div = element.select_one('div#downloadpdf')
        text = div.text
        if 'Downloaded' in text and 'times' in text:
            matches = re.findall(r'Downloaded \d+ times', text)
            for match in matches:
                count = match.replace('Downloaded', '').replace('times', '').strip()
                if count.isdigit():
                    return int(count)

    @staticmethod
    def __read_file_size(element):
        # -> div id='downloadpdf'
        #   -> search text '\d+ MB'
        div = element.select_one('div#downloadpdf')
        text = div.text
        if 'MB' in text:
            matches = re.findall(r'\d+ MB', text)
            for match in matches:
                count = match.replace('MB', '').strip()
                if count.isdigit():
                    return int(count)

    @staticmethod
    def __read_file_url(element):
        # -> div id='downloadpdf'
        #   -> search text '\d+ MB'
        div = element.select_one('div#downloadpdf')
        anchors = div.find_all('a')
        for anchor in anchors:
            if anchor.has_attr('href') and anchor.has_attr('onclick'):
                # TODO: verify thumbnail url integrity
                # TODO: use absolute thumbnail urls
                return anchor.attrs['href']

    @staticmethod
    def __read_id(element):
        # -> a class='leftList' > img
        #   -> search a[href] with 'ID=\d+'
        anchors = element.select('a.leftList > img')
        for anchor in anchors:
            href = anchor.parent['href']
            if 'ID=' in href:
                matches = re.findall(r'ID=\d+', href)
                for match in matches:
                    count = match.replace('ID=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_language(element):
        # -> td > a [href='.....Language=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Language=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_language_id(element):
        # -> td > a [href='.....Language=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            href = anchor.attrs['href']
            if 'Language=' in href:
                matches = re.findall(r'Language=\d+', href)
                for match in matches:
                    count = match.replace('Language=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_name(element):
        # -> <div id='honey' name='NAME' ...>
        div = element.select_one('div#honey')
        if div.has_attr('name'):
            return div.attrs['name'].strip()

    @staticmethod
    def __read_page_breadth(element):
        # -> td > a [href='.....Breadth=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Breadth=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_page_count(element):
        # -> next element after (td > font text='Pages')
        fonts = element.select('td > font')
        for font in fonts:
            if 'Pages' in font.text:
                return font.parent.next_sibling.text.strip()

    @staticmethod
    def __read_page_length(element):
        # -> td > a [href='.....Length=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Length=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_publisher(element):
        # -> td > a [href='.....Publisher=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Publisher=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_publisher_id(element):
        # -> td > a [href='.....Publisher=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            href = anchor.attrs['href']
            if 'Publisher=' in href:
                matches = re.findall(r'Publisher=\d+', href)
                for match in matches:
                    count = match.replace('Publisher=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_publish_year(element):
        # -> td > a [href='.....PublisherYear=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'PublisherYear=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_rating(element):
        # TODO: read rating
        return

    @staticmethod
    def __read_script(element):
        # -> td > a [href='.....Script=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            if 'Script=' in anchor.attrs['href']:
                return anchor.text.strip()

    @staticmethod
    def __read_script_id(element):
        # -> td > a [href='.....Script=.....']
        anchors = element.select('td > a[href]')
        for anchor in anchors:
            href = anchor.attrs['href']
            if 'Script=' in href:
                matches = re.findall(r'Script=\d+', href)
                for match in matches:
                    count = match.replace('Script=', '').strip()
                    if count.isdigit():
                        return int(count)

    @staticmethod
    def __read_sponsor(element):
        # TODO: read sponsor
        # TODO: non-english text not available
        return

    @staticmethod
    def __read_sponsor_id(element):
        # -> td > font text='Digitization Sponsor' > a[href]
        fonts = element.select('td > font')
        for font in fonts:
            if 'Digitization Sponsor' in font.text:
                href = font.parent.find('a').attrs['href']
                if 'ID=' in href:
                    matches = re.findall(r'ID=\d+', href)
                    for match in matches:
                        count = match.replace('ID=', '').strip()
                        if count.isdigit():
                            return int(count)

    @staticmethod
    def __read_thumbnail(element):
        # -> a class='leftList'
        #   -> img
        img = element.find('a', attrs={'class': 'leftList'}).find('img')
        # TODO: verify thumbnail url integrity
        # TODO: use absolute thumbnail urls
        return img.attrs['src']

    @staticmethod
    def verify_book_missing_info(element):
        # TODO: find-missing info tags
        return
