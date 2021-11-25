from pathlib import PurePosixPath
from urllib.parse import urlparse
import os
import requests
import bs4
from bs4 import BeautifulSoup
from requests.models import Response


DIR_PATH = os.getcwd()


def download(url, path=DIR_PATH):
    # dir_name = os.path.join(DIR_PATH, PurePosixPath(path).relative_to('/'))
    # url_to_name = change_url(url)
    path_to_file = os.path.join(DIR_PATH, PurePosixPath(path).relative_to('/'), change_url(url))
    #  dir_for_files_path = os.path.join(dir_name, get_file_dir_name(url_to_name))
    raw_response = requests.get(url)
    raw_response.encoding = 'utf-8'

    with open(path_to_file, 'w+') as file:
        response = BeautifulSoup(raw_response.text, 'html.parser')
        file.write(response.prettify())
    get_image_from_html(path)
    return str(path_to_file)


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def change_url(url):
    new_name = []

    for s in remove_schema(url):
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append('.html')
    return ''.join(new_name)


# def get_file_name(name):
#     new_name = [name, '.html']
#     return ''.join(new_name)


# def get_file_dir_name(name):
#     new_name = [name, '._files']
#     return ''.join(new_name)


def get_image_from_html(path):
    with open(path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for line in soup.find_all('img'):
            print(line.get('src'))