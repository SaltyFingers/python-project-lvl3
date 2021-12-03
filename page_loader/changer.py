import pathlib
from urllib.parse import urljoin, urlparse


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def make_correct_url(main_url, url):
    parsed_url = urlparse(url)
    parsed_main_url = urlparse(main_url)
    if not parsed_url.netloc and not parsed_url.scheme:
        return urljoin(main_url, url)
    elif not parsed_url.scheme:
        return parsed_url.geturl()._replace(scheme=parsed_main_url.scheme)
    else:
        return url


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
    if is_main:
        name.append(f'_{suffix[1:]}')
    else:
        name.append(suffix)
    return ''.join(name)
