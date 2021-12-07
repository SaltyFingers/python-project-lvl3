from os import path
import pathlib
from urllib.parse import urljoin, urlparse, urlunsplit


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def make_absolute_url(main_url, url):
    scheme_and_netloc = urlparse(main_url).scheme + '://' + urlparse(main_url).netloc
    path_and_etc = urlparse(url).path
    return scheme_and_netloc + path_and_etc
                           

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
