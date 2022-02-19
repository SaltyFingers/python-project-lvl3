import pathlib
from urllib.parse import urlparse, urlsplit, urljoin
import os


def remove_schema(url):
    # parsed_url = urlparse(url)
    # scheme = '%s://' % parsed_url.scheme
    # return parsed_url.geturl().replace(scheme, '', 1)
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path


def make_absolute_url(main_url, url):
    split_main_url = urlsplit(main_url)
    split_url = urlsplit(url)
    base = split_main_url.scheme + '://' + split_main_url.netloc
    print(base)
    # absolute_url = split_url._replace(scheme=split_main_url.scheme,
    #                                   netloc=split_main_url.netloc)
    return urljoin(base, split_url.path)


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


def make_name(url, purpose=None):
    url = remove_schema(remove_excess_symbols(url))
    if purpose == 'dir':
        suffix = '_files'
    elif (pathlib.PurePosixPath(url).suffix
          and purpose is None) or purpose == 'file':
        suffix = pathlib.PurePosixPath(url).suffix
        url = url[:-len(suffix)]
    else:
        suffix = '.html'
    name = replace_symbols_with_dashes(url)
    name.append(suffix)
    if purpose == 'file':
        name.append('.html')
    return ''.join(name)


def make_path(path, name):
    return os.path.join(path, name)
