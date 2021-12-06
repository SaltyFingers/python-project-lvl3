import os
from pathlib import PurePosixPath
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.changer import (make_absolute_url,
                                 make_name_from_url)

DIR_PATH = os.getcwd()

link_from_tag = {
    'img': 'src',
    'script': 'src',
    'link': 'href', }

def download(url, path=DIR_PATH):
    if path != DIR_PATH:
        working_dir = os.path.join(DIR_PATH,
                                   PurePosixPath(path).relative_to('/'))
    else:
        working_dir = path
    main_page_name = make_name_from_url(url, is_main=True)
    names = {"main_dir": ''.join([main_page_name, '.html']),
             "files_dir": ''.join([main_page_name, '_files']), }

    path_to_main_file = os.path.join(working_dir, names['main_dir'])
    path_to_files_dir = os.path.join(working_dir, names['files_dir'])

    if not os.path.exists(path_to_files_dir):
        os.mkdir(path_to_files_dir)

    raw_data = requests.get(url)
    raw_data.encoding = 'utf-8'

    with open(path_to_main_file, 'w+') as file:
        page_data = BeautifulSoup(raw_data.text, 'html.parser')
        for line in page_data.find_all(['img', 'link', 'script']):
            main_host = urlparse(url).netloc
            line_url, tag = get_line_url_and_tag(line)
            line_url_host = urlparse(line_url).netloc

            if not line_url or line_url == url or (
                line_url_host and line_url_host != main_host):
                continue

            file_name = make_name_from_url(line_url)
            file_path = os.path.join(path_to_files_dir, file_name)
            absolute_url = make_absolute_url(url, line_url)
            line_data = get_line_data(absolute_url, tag)
            flag = 'ab' if tag == 'img' else 'w+'
            save_file(file_path, flag, line_data)
            # with open(file_path, flag) as inner_file:
            #     inner_file.write(line_data)
            line[link_from_tag[tag]] = file_path 

        file.write(page_data.prettify())
    return str(path_to_main_file)


def save_file(path, flag, data):
    with open(path, flag) as inner_file:
        inner_file.write(data)


def get_line_url_and_tag(line):
    if line.name == 'img':
        return line.get('scr'), line.name
    elif line.name == 'link':
        return line.get('href'), line.name
    elif line.name == 'script' and line.get('scr'):
        return line.get('scr'), line.name
    else:
        return None, None


def get_line_data(obj_url, tag):
    if tag == 'img':
        return requests.get(obj_url).content
    else:
        raw_line_data = requests.get(obj_url)
        raw_line_data.encoding = 'utf-8'
        return BeautifulSoup(raw_line_data.text, 'html.parser').prettify()
