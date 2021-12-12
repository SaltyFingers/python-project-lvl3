import pathlib
from urllib.parse import urlparse, urlsplit, urlunsplit


link_from_tag = {
    'img': 'src',
    'script': 'src',
    'link': 'href', }


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def make_absolute_url(main_url, url):
    split_main_url = urlsplit(main_url)
    split_url = urlsplit(url)
    absolute_url = split_url._replace(scheme=split_main_url.scheme,
                                      netloc=split_main_url.netloc)
    return urlunsplit(absolute_url)


def make_name_from_url(url, is_main=False):
    name = []

    if url.endswith('/'):
        url = url[:-1]

    if not url[0].isalnum():
        url = url[1:]

    if pathlib.PurePosixPath(url).suffix:
        suffix = pathlib.PurePosixPath(url).suffix
        range_ = remove_schema(url)[:-len(suffix)]
    else:
        suffix = '.html'
        range_ = remove_schema(url)

    for s in range_:
        if not s.isalnum():
            name.append('-')
        else:
            name.append(s)
    if not is_main:
        name.append(suffix)
    return ''.join(name)


def change_url(line, tag, file_path):
    line[link_from_tag[tag]] = file_path
    return line
