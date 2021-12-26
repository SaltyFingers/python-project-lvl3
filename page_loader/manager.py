import sys
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from page_loader.logger import get_logger

logger = get_logger(__name__)


def save_file(path, flag, data):
    try:
        file = open(path, flag)
    except OSError as error:
        logger.error(f'Error occured: {error}!')
        sys.exit('An error occured! Cat\'t save file!')
    else:
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


def get_page_data(url):
    data = requests.get(url)
    response = data.raise_for_status()
    if response != 200:
        logger.error(f'Response error occured: code {response}')
        sys.exit('Response error occured! Work stopped!')
    data.encoding = 'utf-8'
    page_data = BeautifulSoup(data.text, 'html.parser')
    return page_data


def get_line_data(obj_url, tag):
    # try:
    #     response = requests.get(obj_url)
    #     response.raise_for_status()
    # except HTTPError as http_error:
    #     logger.error(f'HTTP error occurred with inner resource: '
    #                  f'{http_error}! Work stopped!')
    #     sys.exit('HTTP error occurred with inner resource!')
    # except Exception as error:
    #     logger.error(f'Error occured with inner resource: '
    #                  f'{error}! Work stopped!')
    #     sys.exit('Error occurred with inner resource!')
    data = requests.get(obj_url)
    response = data.raise_for_status()
    if response != 200:
        logger.error(f'Resource response error occured: code {response}')
        sys.exit('Resource response error occured! Work stopped!')
    if tag == 'img':
        return data.content
    else:
        data.encoding = 'utf-8'
        return BeautifulSoup(data.text, 'html.parser').prettify()
