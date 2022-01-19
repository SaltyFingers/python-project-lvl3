import os
from urllib.parse import urlparse

import requests
import bs4
# from bs4 import BeautifulSoup
from progress.bar import Bar
from requests.exceptions import HTTPError, SSLError

from page_loader.changer import (make_absolute_url, make_main_name,
                                 make_new_line)
from page_loader.logger import get_logger

logger = get_logger(__name__)


def create_dir_for_files(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except PermissionError as error:
        logger.error(f'Permission error: {error}')
        print('You don\'t have permission!')
        raise
    except OSError as e:
        logger.error(f'Another error occured: {e}')
        print('Couldn\'t create a directory for files!')
        raise


def save_file(path, flag, data):
    try:
        file = open(path, flag)
    except PermissionError as error:
        logger.error(f'Permission error occured: {error}!')
        print('You don\'t have permission!')
        raise
    except FileNotFoundError as error:
        logger.error(f'Directory {path} does not exists! Error: {error}')
        print('Directory does not exists!')
        raise
    file.write(data)
    file.close()


def get_line_url_and_tag(line):
    if line.name == 'img':
        return line.get('src'), line.name
    elif line.name == 'link':
        return line.get('href'), line.name
    elif line.name == 'script' and line.get('src'):
        return line.get('src'), line.name
    else:
        return None, None


def get_data(url, tag=None):
    try:
        data = requests.get(url)
    except SSLError as ssl_error:
        logger.error(f'SSL error occurred: {ssl_error} with {url}!')
        print(f'SSL error occurred with {url}')
        raise
    except HTTPError as http_error:
        logger.error(f'HTTP error occurred: {http_error} with {url}!')
        print(f'HTTP error occurred with {url}')
        raise
    except Exception as error:
        logger.error(f'An error occurred: {error} with {url}!')
        print(f'An error occurred with {url}')
        raise

    if tag == 'img':
        return data.content
    elif tag == 'link' or tag == 'script':
        return bs4.BeautifulSoup(data.text, 'html.parser').prettify()
    else:
        return bs4.BeautifulSoup(data.text, 'html.parser')


def is_any_resources(url, resources):
    is_iner_res_bool_list = []
    for line in resources:
        line_url = get_line_url_and_tag(line)[1]
        is_iner_res_bool_list.append(is_proper_to_download(url, line_url))
    return any(is_iner_res_bool_list)


def is_proper_to_download(url, line_url):
    main_host = urlparse(url).netloc
    line_url_host = urlparse(line_url).netloc
    return (line_url or line_url != url or (
            line_url_host and line_url_host == main_host))


def download_resources(url, data, path_to_files_dir):
    bar = Bar('Downloading resouces ',
              max=len(data.find_all(['img', 'link', 'script'])))
    for line in data.find_all(['img', 'link', 'script']):
        line_url, tag = get_line_url_and_tag(line)
        absolute_url = make_absolute_url(url, line_url)
        if not is_proper_to_download(url, line_url):
            bar.next()
            continue
        file_name = make_main_name(line_url)
        file_path = os.path.join(path_to_files_dir, file_name)
        logger.info(f'Downloading {absolute_url}')
        line_data = get_data(absolute_url, tag)
        flag = 'wb' if tag == 'img' else 'w+'
        save_file(file_path, flag, line_data)
        logger.info('File successfully downloaded!')
        line = make_new_line(line, tag, file_path)
        bar.next()
    bar.finish()
