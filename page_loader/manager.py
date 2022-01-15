import os
import sys

import requests
from bs4 import BeautifulSoup

from page_loader.logger import get_logger

logger = get_logger(__name__)


def save_file(path, flag, data):
    try:
        file = open(path, flag)
    except PermissionError as error:
        logger.error(f'Permission error occured: {error}!')
        sys.exit('You don\'t have permission!')
    except FileNotFoundError as error:
        logger.error(f'Directory {path} does not exists! Error: {error}')
        sys.exit('Directory does not exists!')
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
    except Exception as error:
        logger.error(f'Connection error occured: {error}')
        sys.exit(f'An error occured with {url}')
    if tag == 'img':
        return data.content
    elif tag == 'link' or tag == 'script':
        return BeautifulSoup(data.text, 'html.parser').prettify()
    else:
        return BeautifulSoup(data.text, 'html.parser')


def create_dir_for_files(path):
    try:
        os.mkdir(path)
    except PermissionError as error:
        logger.error(f'Permission error: {error}')
        sys.exit('You don\'t have permission!')
    except FileExistsError:
        pass
    if not os.path.exists(path):
        logger.error('Directory for files does not exist after creating!')
        sys.exit('An error occured with direcrory for files!')
