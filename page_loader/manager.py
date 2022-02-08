import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from requests.exceptions import (ConnectionError, ConnectTimeout, HTTPError,
                                 SSLError)

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
        raise PermissionError('You don\'t have permission!')

    except OSError as e:
        logger.error(f'Another error occured: {e}')
        raise OSError('Couldn\'t create a directory for files!')


def save_file(path, flag, data):
    try:
        with open(path, flag) as file:
            file.write(data)

    except PermissionError as error:
        logger.error(f'Permission error occured: {error}!')
        raise PermissionError('You don\'t have permission!')

    except FileNotFoundError as error:
        logger.error(f'Can\'t save file {path}! Error: {error}')
        raise FileNotFoundError(f'Can\'t save file {path}!')


def get_line_url_and_tag(line):
    if line.name == 'img':
        return line.get('src'), line.name
    elif line.name == 'link':
        return line.get('href'), line.name
    elif line.name == 'script' and line.get('src'):
        return line.get('src'), line.name
    else:
        return None


def get_data(url, tag=None):
    try:
        response = requests.get(url)
        status = response.status_code
    except SSLError as ssl_error:
        logger.error(f'SSL error occurred: {ssl_error} with {url}!')
        raise SSLError(f'SSL error occurred with {url}')

    except HTTPError as http_error:
        logger.error(f'HTTP error occurred: {http_error} with {url}!')
        raise HTTPError(f'HTTP error occurred with {url}')

    except ConnectTimeout as error:
        logger.error(f'{url} connection timeout: {error}')
        raise ConnectTimeout('Connection Timeout!')

    if status != 200:
        logger.error(f'{url} - Status code is not 200! It\'s {status}!')
        raise ConnectionError(f'Responce code is not 200! It\'s: {status}')

    if tag == 'img':
        return response.content
    elif tag == 'link' or tag == 'script':
        return response.content
    else:
        return BeautifulSoup(response.content, 'html.parser')


def check_output_dir(path):
    if not os.path.exists(path):
        logger.error(f'Output directory {path} does not exist!')
        raise FileNotFoundError('Output directory does not exists!')


def is_any_resources(url, resources):
    is_iner_res_bool_list = []
    for line in resources:
        line_url = get_line_url_and_tag(line)[1]
        is_iner_res_bool_list.append(is_proper_to_download(url, line_url))
    return any(is_iner_res_bool_list)


def is_proper_to_download(url, line_url):
    main_host = urlparse(url).netloc
    line_url_host = urlparse(line_url).netloc
    return (line_url and line_url != url
            and (line_url_host in main_host)
            or not line_url_host)


def download_resources(url, data, path_to_files_dir):
    downloaded_resources = []
    bar = Bar('Downloading resouces ',
              max=len(data.find_all(['img', 'link', 'script'])))
    for line in data.find_all(['img', 'link', 'script']):
        if get_line_url_and_tag(line) is None:
            continue
        line_url, tag = get_line_url_and_tag(line)
        absolute_url = make_absolute_url(url, line_url)
        if is_proper_to_download(url, line_url):
            file_name = make_main_name(absolute_url)
            file_path = os.path.join(path_to_files_dir, file_name)
            logger.info(f'Downloading {absolute_url}')
            try:
                line_data = get_data(absolute_url, tag)
                flag = 'wb' if isinstance(line_data, bytes) else 'w'
                save_file(file_path, flag, line_data)
            except Exception as e:
                logger.warning(f'Can\'t download {absolute_url}, error: {e}')
                print(f'Can\'t download {absolute_url}')
                bar.next()
                downloaded_resources.append('- ' + absolute_url)
                continue
            else:
                logger.info('File successfully downloaded!')
                line = make_new_line(line, tag, file_path)
                downloaded_resources.append('+ ' + absolute_url)
        bar.next()
    bar.finish()
    print('\n'.join(downloaded_resources))
