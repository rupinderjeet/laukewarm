import re


def read_book(document):
    left_pane = document.find('td', attrs={'width': '31%', 'valign': 'top', 'height': '300'})
    right_pane = document.find('td', attrs={'width': '69%', 'valign': 'top'})
    book = {
        'accession_code': __read_accession_code(right_pane),
        'author_name': __read_author_name(right_pane),
        'author_id': __read_author_id(right_pane),
        'completion': __read_completion_status(right_pane),
        'condition': __read_condition(right_pane),
        'custodian_name': __read_custodian_name(right_pane),
        'custodian_id': __read_custodian_id(right_pane),
        'download_count': __read_download_count(left_pane),
        'file_size': __read_file_size(left_pane),
        'file_url': __read_file_url(left_pane),
        'id': __read_id(left_pane),
        'language': __read_language(right_pane),
        'language_id': __read_language_id(right_pane),
        'name': __read_name(document),
        'page_breadth': __read_page_breadth(right_pane),
        'page_count': __read_page_count(right_pane),
        'page_length': __read_page_length(right_pane),
        'publisher': __read_publisher(right_pane),
        'publisher_id': __read_publisher_id(right_pane),
        'publish_year': __read_publish_year(right_pane),
        'rating': __read_rating(left_pane),
        'script': __read_script(right_pane),
        'script_id': __read_script_id(right_pane),
        'sponsor': __read_sponsor(right_pane),
        'sponsor_id': __read_sponsor_id(right_pane),
        'thumbnail': __read_thumbnail(left_pane),
    }
    verify_book_missing_info(document)
    return book


def __read_accession_code(element):
    # -> next element after (td > font text='Accession Number')
    fonts = element.select('td > font')
    for font in fonts:
        if 'Accession Number' in font.text:
            return font.parent.text.replace('Accession Number', '').strip()


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


def __read_author_name(element):
    # -> td > a [href='.....Author=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Author=' in anchor.attrs['href']:
            return anchor.text.strip()


def __read_completion_status(element):
    # -> td > a [href='.....Completion=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Completion=' in anchor.attrs['href']:
            return anchor.text.strip()


def __read_condition(element):
    # -> td > a [href='.....DocCondition=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'DocCondition=' in anchor.attrs['href']:
            return anchor.text.strip()


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


def __read_custodian_name(element):
    # -> td > a [href='.....Contributor=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Contributor=' in anchor.attrs['href']:
            return anchor.text.strip()


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


def __read_language(element):
    # -> td > a [href='.....Language=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Language=' in anchor.attrs['href']:
            return anchor.text.strip()


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


def __read_name(element):
    # -> <div id='honey' name='NAME' ...>
    div = element.select_one('div#honey')
    if div.has_attr('name'):
        return div.attrs['name'].strip()


def __read_page_breadth(element):
    # -> td > a [href='.....Breadth=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Breadth=' in anchor.attrs['href']:
            return anchor.text.strip()


def __read_page_count(element):
    # -> next element after (td > font text='Pages')
    fonts = element.select('td > font')
    for font in fonts:
        if 'Pages' in font.text:
            return font.parent.next_sibling.text.strip()


def __read_page_length(element):
    # -> td > a [href='.....Length=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Length=' in anchor.attrs['href']:
            return anchor.text.strip()


def __read_publisher(element):
    # -> td > a [href='.....Publisher=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Publisher=' in anchor.attrs['href']:
            return anchor.text.strip()


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


def __read_publish_year(element):
    # -> td > a [href='.....PublisherYear=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'PublisherYear=' in anchor.attrs['href']:
            return anchor.text.strip()


def __read_rating(element):
    # TODO: read rating
    return


def __read_script(element):
    # -> td > a [href='.....Script=.....']
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Script=' in anchor.attrs['href']:
            return anchor.text.strip()


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


def __read_sponsor(element):
    # TODO: read sponsor
    # TODO: non-english text not available
    return


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


def __read_thumbnail(element):
    # -> a class='leftList'
    #   -> img
    img = element.find('a', attrs={'class': 'leftList'}).find('img')
    # TODO: verify thumbnail url integrity
    # TODO: use absolute thumbnail urls
    return img.attrs['src']


def verify_book_missing_info(element):
    # TODO: find-missing info tags
    return
