import pathlib
from urllib.parse import urlparse, urlsplit, urlunsplit
import os


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


def remove_excess_symbols(url):
    if url.endswith('/'):
        url = url[:-1]
    if not url[0].isalnum():
        url = url[1:]
    return url


def replace_symbols_with_dashes(url):
    name = []
    for s in url:
        if not s.isalnum():
            name.append('-')
        else:
            name.append(s)
    return name


def make_main_name(url, is_main=False):
    url = remove_excess_symbols(url)

    if pathlib.PurePosixPath(url).suffix:
        suffix = pathlib.PurePosixPath(url).suffix
        new_url = remove_schema(url)[:-len(suffix)]
    else:
        suffix = '.html'
        new_url = remove_schema(url)
    name = replace_symbols_with_dashes(new_url)
    if not is_main:
        name.append(suffix)
    return ''.join(name)


def make_names(path, main_name):
    path_to_main_file = os.path.join(path, main_name + '.html')
    path_to_files_dir = os.path.join(path, main_name + '_files')
    return path_to_main_file, path_to_files_dir


def make_new_line(line, tag, file_path):
    link_from_tag = {
        'img': 'src',
        'script': 'src',
        'link': 'href', }
    line[link_from_tag[tag]] = file_path
    return line
