from pathlib import PurePath, PurePosixPath
from urllib.parse import urljoin, urlparse
import os

DIR_SUFFIX = '_files'
HTML_SUFFIX = '.html'


def make_path(path, name):
    return PurePath(path, name)


def remove_schema(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path


def make_absolute_url(main_url, url):
    return urljoin(main_url, url)


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


def make_dir_name(url):
    new_url = replace_symbols_with_dashes(remove_schema(
                                          remove_excess_symbols(url)))
    return new_url + DIR_SUFFIX


def make_file_name(url, is_output_file=False):
    name = []
    new_url = remove_schema(remove_excess_symbols(url))
    if is_output_file or (PurePosixPath(new_url).suffix
                          and not is_output_file):
        new_url, suffix = os.path.splitext(new_url)
    else:
        suffix = HTML_SUFFIX
    name.append(replace_symbols_with_dashes(new_url))
    name.append(suffix)
    if is_output_file:
        name.append(HTML_SUFFIX)
    return ''.join(name)
