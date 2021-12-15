import os
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.changer import (change_url, make_absolute_url,
                                 make_name_from_url)
from page_loader.logger import get_logger
from page_loader.manager import get_line_data, get_line_url_and_tag, save_file

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):

    if not os.path.exists(path):
        logger.error(f'Directory {path} does not exist!')
        sys.exit('Directory does not exist! Work stopped!')

    logger.info(f'Start downloading {url} to {path}')

    main_page_name = make_name_from_url(url, is_main=True)
    names = {"main_dir": ''.join([main_page_name, '.html']),
             "files_dir": ''.join([main_page_name, '_files']), }

    path_to_main_file = os.path.join(path, names['main_dir'])
    path_to_files_dir = os.path.join(path, names['files_dir'])

    logger.info('Creating directory for files')
    if not os.path.exists(path_to_files_dir):
        try:
            os.mkdir(path_to_files_dir)
        except OSError as err:
            logger.error(err)
            sys.exit('Can\'t create directory for files! Work stopped!')
        logger.info(f'Directory {path_to_files_dir} successfully created!')
    else:
        logger.info(f'Directory {path_to_files_dir} '
                    f'has already exists! Continue!')

    raw_data = requests.get(url)
    raw_data.encoding = 'utf-8'
    page_data = BeautifulSoup(raw_data.text, 'html.parser')
    logger.info('Start downloading inner resources')

    for line in page_data.find_all(['img', 'link', 'script']):
        main_host = urlparse(url).netloc
        line_url, tag = get_line_url_and_tag(line)
        line_url_host = urlparse(line_url).netloc

        if not line_url or line_url == url or (
                line_url_host and line_url_host != main_host):
            continue

        logger.info(f'Downloading {line_url} to {path_to_files_dir}')

        file_name = make_name_from_url(line_url)
        file_path = os.path.join(path_to_files_dir, file_name)
        absolute_url = make_absolute_url(url, line_url)
        line_data = get_line_data(absolute_url, tag)
        flag = 'ab' if tag == 'img' else 'w+'
        save_file(file_path, flag, line_data)
        line = change_url(line, tag, file_path)

    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, 'w+', page_data.prettify())
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)
