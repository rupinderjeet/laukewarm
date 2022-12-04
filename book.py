import re


def read_books(soup):
    # -> <td width="233" valign="middle" height="200">
    results = soup.find_all("td", attrs={"width": "233", "valign": "middle", "height": "200"})
    print(f"total books are {len(results)}")

    books = []
    for result in results:
        book = read_book(result)
        books.append(book)

    print(f'books: {len(books)}')


def read_book(soup):
    book = {
        'author': read_book_author(soup),
        'id': read_book_id(soup),
        'name': read_book_name(soup),
        'page_count': read_book_page_count(soup),
        'publisher': read_book_publisher(soup),
        'publish_year': read_book_publish_year(soup),
        'rating': read_book_rating(soup),
        'script': read_book_script(soup),
        'thumbnail': read_book_thumbnail(soup),
    }
    verify_book_missing_info(soup)
    return book


def read_book_author(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a href="#" title="Author"
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', attrs={"href": "#", "title": 'Author'})
        if anchor_tag:
            return anchor_tag.string.strip()


def read_book_id(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a class="leftList" href
    #      -> search text 'ID=\d+'
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', class_="leftList")
        if anchor_tag:
            text = anchor_tag.attrs['href'].strip()
            if 'ID=' in text:
                matches = re.findall(r'ID=\d+', text)
                for match in matches:
                    count = match.replace('ID=', '').strip()
                    if count.isdigit():
                        return int(count)


def read_book_name(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a class="leftList"
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', class_="leftList")
        if anchor_tag:
            return anchor_tag.string.strip()


def read_book_page_count(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> search text '\d+ pages'
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        text = td_tag.text
        if 'pages' in text:
            matches = re.findall(r'\d+ pages', text)
            for match in matches:
                count = match.replace('pages', '').strip()
                if count.isdigit():
                    return int(count)


def read_book_publisher(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a href="#" title="Publisher"
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', attrs={"href": "#", "title": 'Publisher'})
        if anchor_tag:
            return anchor_tag.string.strip()


def read_book_publish_year(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a href="#" title="PublisherYear"
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', attrs={"href": "#", "title": 'PublisherYear'})
        if anchor_tag:
            return anchor_tag.string.strip()


def read_book_rating(soup):
    # -> search 'img' tags with 'name' & 'src' (must end in 'withoutRating.gif')
    img_tags = soup.find_all("img")
    matching_img_tags = [img_tag for img_tag in img_tags
                         if img_tag.has_attr('name')
                         and img_tag.has_attr('src')
                         and img_tag.attrs['src'].endswith('withoutRating.gif')]
    return len(matching_img_tags)


def read_book_script(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a href="#" title="Script"
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tag = td_tag.find('a', attrs={"href": "#", "title": 'Script'})
        if anchor_tag:
            return anchor_tag.string.strip()


def read_book_thumbnail(soup):
    # -> <td height="95" valign="middle" align="center">
    #   -> a
    #     -> img
    td_tags = soup.find_all("td", attrs={"height": "95", "valign": "middle", "align": "center"})
    for td_tag in td_tags:
        img_tag = td_tag.find('a').find('img')
        if img_tag:
            # TODO: verify thumbnail url integrity
            # TODO: use absolute thumbnail urls
            return img_tag.attrs['src']


def verify_book_missing_info(soup):
    # -> <td width="100%" colspan="2" height="25">
    #   -> a href="#"
    #       -> not 'title' contains 'Author|Publisher|PublisherYear|Script'
    td_tags = soup.find_all("td", attrs={"width": "100%", "colspan": "2", "height": "25"})
    for td_tag in td_tags:
        anchor_tags = td_tag.find_all('a', attrs={"href": "#"})
        for anchor_tag in anchor_tags:
            if anchor_tag.attrs['title'] in 'Author|Publisher|PublisherYear|Script':
                continue
            print(f"missing-info: {anchor_tag}")
