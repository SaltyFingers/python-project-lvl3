from pathlib import PurePosixPath
import pathlib
from urllib.parse import urljoin, urlparse
import os
import requests
from bs4 import BeautifulSoup


DIR_PATH = os.getcwd()


def download(url, path=DIR_PATH):
    if path != DIR_PATH:
        working_dir = os.path.join(DIR_PATH,
                                   PurePosixPath(path).relative_to('/'))
    else:
        working_dir = path

    names = {"main_dir": ''.join([make_name_from_url(url), '.html']),
             "files_dir": ''.join([make_name_from_url(url), '_files']),
             }

    path_to_file = os.path.join(working_dir, names['main_dir'])
    files_dir = os.path.join(working_dir, names['files_dir'])

    if not os.path.exists(files_dir):
        os.mkdir(files_dir)

    raw_response = requests.get(url)
    raw_response.encoding = 'utf-8'

    with open(path_to_file, 'w+') as file:
        response = BeautifulSoup(raw_response.text, 'html.parser')
        for line in response.find_all('img'):
            img_url = line.get('src')
            img_name = make_img_name(img_url)
            line['src'] = os.path.join(files_dir, img_name)
            with open(os.path.join(files_dir, img_name), 'ab') as image:
                image.write(requests.get(make_correct_img_url(
                            url, img_url)).content)
        file.write(response.prettify())
    return str(path_to_file)


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def make_correct_img_url(url, img_url):
    parsed_img_url = urlparse(img_url)
    parsed_url = urlparse(url)
    if not parsed_img_url.netloc and not parsed_img_url.scheme:
        return urljoin(url, img_url)
    elif not parsed_img_url.scheme:
        return parsed_img_url.geturl()._replace(scheme=parsed_url.scheme)
    else:
        return img_url


def make_name_from_url(url):
    page_name = []
    if url.endswith('/'):
        url = url[:-1]
    for s in remove_schema(url):
        if not s.isalnum():
            page_name.append('-')
        else:
            page_name.append(s)
    return ''.join(page_name)


def make_img_name(image):
    new_name = []
    if image.startswith('/'):
        image = image[1:]
    suffix = pathlib.PurePosixPath(image).suffix
    for s in remove_schema(image)[:-len(suffix)]:
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append(suffix)
    return ''.join(new_name)
