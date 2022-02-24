from pathlib import PurePath, PurePosixPath
from urllib.parse import urljoin, urlparse, urlsplit
import os


def remove_schema(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path


def make_absolute_url(main_url, url):
    split_main_url = urlsplit(main_url)
    split_url = urlsplit(url)
    base_url = split_main_url.scheme + '://' + split_main_url.netloc
    return urljoin(base_url, split_url.path)


def remove_excess_symbols(url):
    if url.endswith('/'):
        url = url[:-1]
    if not url[0].isalnum():
        url = url[1:]
    return url


def replace_symbols_with_dashes(url):
    new_url = []
    for symbol in url:
        if not symbol.isalnum():
            new_url.append('-')
        else:
            new_url.append(symbol)
    return ''.join(new_url)


def make_base_name(url, purpose):
    name = []
    new_url = remove_schema(remove_excess_symbols(url))

    if purpose == 'directory':
        suffix = '_files'
    elif purpose == 'output_file':
        new_url, suffix = os.path.splitext(new_url)

    name.append(replace_symbols_with_dashes(new_url))
    name.append(suffix)

    if purpose == 'output_file':
        name.append('.html')

    return ''.join(name)


def make_name(url):
    name = []
    new_url = remove_schema(remove_excess_symbols(url))

    if PurePosixPath(new_url).suffix:
        new_url, suffix = os.path.splitext(new_url)
    else:
        suffix = '.html'

    name.append(replace_symbols_with_dashes(new_url))
    name.append(suffix)

    return ''.join(name)


def make_path(path, name):
    return PurePath(path, name)
