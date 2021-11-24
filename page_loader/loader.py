from pathlib import PurePosixPath
from urllib.parse import urlparse
import os

DIR_PATH = os.getcwd()


def download(url, path=DIR_PATH):
    path_to_file = os.path.join(DIR_PATH, PurePosixPath(path).relative_to('/'),
                                get_file_name(url))
    with open(path_to_file, 'w+'):
        pass
    print(path_to_file)
    return str(path_to_file)


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def get_file_name(url):
    new_name = []

    for s in remove_schema(url):
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append('.html')
    return ''.join(new_name)
