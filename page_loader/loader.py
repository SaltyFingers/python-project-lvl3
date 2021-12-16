import os
import sys
from urllib.parse import urlparse
from progress.spinner import PieSpinner 
import requests
from bs4 import BeautifulSoup

from page_loader.changer import (change_url, make_absolute_url,
                                 make_name_from_url)
from page_loader.logger import get_logger
from page_loader.manager import (get_line_data, get_line_url_and_tag,
                                 get_page_data, save_file)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):
    if not os.path.exists(path):
        logger.error(f'Output directory {path} does not exist!')
        sys.exit('Output directory does not exist! Work stopped!')

    logger.info(f'Start downloading {url} to {path}')

    main_page_name = make_name_from_url(url, is_main=True)
    path_to_main_file = os.path.join(path, main_page_name + '.html')
    path_to_files_dir = os.path.join(path, main_page_name + '_files')

    page_data = get_page_data(url)

    logger.info('Start downloading inner resources')

    main_host = urlparse(url).netloc
    
    
    for line in page_data.find_all(['img', 'link', 'script']):
        
        line_url, tag = get_line_url_and_tag(line)
        line_url_host = urlparse(line_url).netloc
        if not line_url or line_url == url or (
                line_url_host and line_url_host != main_host):
            continue
        with PieSpinner('Processing', max=100) as bar:
            file_path = download_inner_resource_and_get_path(url, line_url, path_to_files_dir, tag)
            bar.next()
        line = change_url(line, tag, file_path)
            

    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, 'w+', page_data.prettify())
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)


def download_inner_resource_and_get_path(url, line_url,
                                         path_to_files_dir, tag):
    
    file_name = make_name_from_url(line_url)
    file_path = os.path.join(path_to_files_dir, file_name)
    absolute_url = make_absolute_url(url, line_url)
    logger.info(f'Downloading {absolute_url}')
    line_data = get_line_data(absolute_url, tag)
    flag = 'ab' if tag == 'img' else 'w+'
    save_file(file_path, flag, line_data)
    return file_path