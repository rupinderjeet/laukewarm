import re


def read_book(soup):
    left_pane = soup.find("td", attrs={"width": "31%", "valign": "top", 'height': '300'})
    right_pane = soup.find("td", attrs={"width": "69%", "valign": "top"})
    book = {
        'accession_code': read_book_accession_code(right_pane),
        'author': read_book_author(right_pane),
        'author_id': read_book_author_id(right_pane),
        'completion': read_book_completion(right_pane),
        'condition': read_book_condition(right_pane),
        'custodian': read_book_custodian(right_pane),
        'custodian_id': read_book_custodian_id(right_pane),
        'download_count': read_book_download_count(left_pane),
        'file_size': read_book_file_size(left_pane),
        'file_url': read_book_file_url(left_pane),
        'id': read_book_id(left_pane),
        'language': read_book_language(right_pane),
        'language_id': read_book_language_id(right_pane),
        'name': read_book_name(soup),
        'page_breadth': read_book_page_breadth(right_pane),
        'page_count': read_book_page_count(right_pane),
        'page_length': read_book_page_length(right_pane),
        'publisher': read_book_publisher(right_pane),
        'publisher_id': read_book_publisher_id(right_pane),
        'publish_year': read_book_publish_year(right_pane),
        # 'rating': read_book_rating(soup),
        'script': read_book_script(right_pane),
        'script_id': read_book_script_id(right_pane),
        'sponsor': read_book_sponsor(right_pane),
        'sponsor_id': read_book_sponsor_id(right_pane),
        'thumbnail': read_book_thumbnail(left_pane),
    }
    verify_book_missing_info(soup)
    return book


def read_book_accession_code(element):
    # -> next element after (td > font text='Accession Number')
    children = element.select("td > font")
    for child in children:
        if 'Accession Number' in child.text:
            return child.parent.text.replace('Accession Number', '').strip()


def read_book_author(element):
    # -> td > a [href=".....Author=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Author=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_author_id(element):
    # -> td > a [href=".....Author=ID....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        href = anchor.attrs['href']
        if 'Author=' in href:
            matches = re.findall(r'Author=\d+', href)
            for match in matches:
                count = match.replace('Author=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_completion(element):
    # -> td > a [href=".....Completion=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Completion=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_condition(element):
    # -> td > a [href=".....DocCondition=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'DocCondition=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_custodian(element):
    # -> td > a [href=".....Contributor=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Contributor=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_custodian_id(element):
    # -> td > a [href=".....Contributor=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        href = anchor.attrs['href']
        if 'Contributor=' in href:
            matches = re.findall(r'Contributor=\d+', href)
            for match in matches:
                count = match.replace('Contributor=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_download_count(soup):
    # -> div id="downloadpdf"
    #   -> search text 'Downloaded \d+ times'
    div_tag = soup.find("div", id='downloadpdf')
    text = div_tag.text
    if 'Downloaded' in text and 'times' in text:
        matches = re.findall(r'Downloaded \d+ times', text)
        for match in matches:
            count = match.replace('Downloaded', '').replace('times', '').strip()
            if count.isdigit():
                return int(count)


def read_book_file_size(soup):
    # -> div id="downloadpdf"
    #   -> search text '\d+ MB'
    div_tag = soup.find("div", id='downloadpdf')
    text = div_tag.text
    if 'MB' in text:
        matches = re.findall(r'\d+ MB', text)
        for match in matches:
            count = match.replace('MB', '').strip()
            if count.isdigit():
                return int(count)


def read_book_file_url(soup):
    # -> div id="downloadpdf"
    #   -> search text '\d+ MB'
    div_tag = soup.find("div", id='downloadpdf')
    anchor_tags = div_tag.find_all('a')
    for anchor_tag in anchor_tags:
        if anchor_tag.has_attr('href') and anchor_tag.has_attr('onclick'):
            # TODO: verify thumbnail url integrity
            # TODO: use absolute thumbnail urls
            return anchor_tag.attrs['href']


def read_book_id(soup):
    # -> a class="leftList" > img
    #   -> search a[href] with 'ID=\d+'
    anchors = soup.select('a.leftList > img')
    for anchor in anchors:
        href = anchor.parent['href']
        if 'ID=' in href:
            matches = re.findall(r'ID=\d+', href)
            for match in matches:
                count = match.replace('ID=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_language(element):
    # -> td > a [href=".....Language=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Language=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_language_id(element):
    # -> td > a [href=".....Language=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        href = anchor.attrs['href']
        if 'Language=' in href:
            matches = re.findall(r'Language=\d+', href)
            for match in matches:
                count = match.replace('Language=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_name(soup):
    # -> <div id="honey" name="NAME" ...>
    child = soup.select_one('div#honey')
    if child.has_attr('name'):
        return child.attrs['name'].strip()


def read_book_page_breadth(element):
    # -> td > a [href=".....Breadth=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Breadth=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_page_count(element):
    # -> next element after (td > font text='Pages')
    children = element.select("td > font")
    for child in children:
        if 'Pages' in child.text:
            return child.parent.next_sibling.text.strip()


def read_book_page_length(element):
    # -> td > a [href=".....Length=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Length=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_publisher(element):
    # -> td > a [href=".....Publisher=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Publisher=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_publisher_id(element):
    # -> td > a [href=".....Publisher=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        href = anchor.attrs['href']
        if 'Publisher=' in href:
            matches = re.findall(r'Publisher=\d+', href)
            for match in matches:
                count = match.replace('Publisher=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_publish_year(element):
    # -> td > a [href=".....PublisherYear=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'PublisherYear=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_rating(soup):
    # -> search 'img' tags with 'name' & 'src' (must end in 'withoutRating.gif')
    img_tags = soup.find_all("img")
    matching_img_tags = [img_tag for img_tag in img_tags
                         if img_tag.has_attr('name')
                         and img_tag.has_attr('src')
                         and img_tag.attrs['src'].endswith('withoutRating.gif')]
    return len(matching_img_tags)


def read_book_script(element):
    # -> td > a [href=".....Script=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        if 'Script=' in anchor.attrs['href']:
            return anchor.text.strip()


def read_book_script_id(element):
    # -> td > a [href=".....Script=....."]
    anchors = element.select('td > a[href]')
    for anchor in anchors:
        href = anchor.attrs['href']
        if 'Script=' in href:
            matches = re.findall(r'Script=\d+', href)
            for match in matches:
                count = match.replace('Script=', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_sponsor(element):
    # -> td (font text='Digitization Sponsor') > a
    return


def read_book_sponsor_id(element):
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


def read_book_thumbnail(soup):
    # -> a class="leftList"
    #   -> img
    img_tag = soup.find("a", attrs={"class": "leftList"}).find('img')
    # TODO: verify thumbnail url integrity
    # TODO: use absolute thumbnail urls
    return img_tag.attrs['src']


def verify_book_missing_info(soup):
    # TODO: find-missing info tags
    return
