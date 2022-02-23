from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from requests.exceptions import (ConnectionError, ConnectTimeout, HTTPError,
                                 SSLError)

from page_loader.changer import change_path
from page_loader.files_manager import save_file
from page_loader.logger import get_logger
from page_loader.namer import make_absolute_url, make_name, make_path

logger = get_logger(__name__)


def get_url_and_name_from_tag(tag_object):
    if tag_object.name == 'img':
        return tag_object.get('src'), tag_object.name
    elif tag_object.name == 'link':
        return tag_object.get('href'), tag_object.name
    elif tag_object.name == 'script' and tag_object.get('src'):
        return tag_object.get('src'), tag_object.name
    else:
        return None


def get_response(url):
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
    return response


def parse_data(data, tag=None):
    if tag:
        return data.content
    else:
        return BeautifulSoup(data.content, 'html.parser')


def is_any_resources(url, resources):
    is_iner_res_bool_list = []
    for line in resources:
        line_url = get_url_and_name_from_tag(line)[1]
        is_iner_res_bool_list.append(is_proper_to_download(url, line_url))
    return any(is_iner_res_bool_list)


def is_proper_to_download(url, line_url):
    main_host = urlparse(url).netloc
    line_url_host = urlparse(line_url).netloc
    return (line_url and line_url != url
            and (line_url_host in main_host)
            or not line_url_host)


def download_resources(url, parsed_data, path_to_files_dir):
    resources = parsed_data.find_all(['img', 'link', 'script'])
    bar = Bar('Downloading resouces ', max=len(resources))
    for resource_tag in resources:
        if get_url_and_name_from_tag(resource_tag) is None:
            continue
        # поменять имена переменных ниже
        tag_url, tag_name = get_url_and_name_from_tag(resource_tag)
        # ------------------------------
        absolute_url = make_absolute_url(url, tag_url)
        if not is_proper_to_download(url, tag_url):
            continue
        file_name = make_name(absolute_url)
        file_path = make_path(path_to_files_dir, file_name)
        logger.info(f'Downloading {absolute_url}')
        try:
            # поменять имена переменных ниже
            resource_content = get_response(absolute_url)
            parsed_resource_content = parse_data(resource_content,
                                                 resource_tag)
            # ------------------------------
            save_file(file_path, parsed_resource_content)
        except Exception as e:
            logger.warning(f'Can\'t download {absolute_url}, error: {e}')
            continue
        else:
            logger.info(f'{absolute_url} successfully downloaded!')
            change_path(resource_tag, tag_name, file_path)
        bar.next()
    bar.finish()
