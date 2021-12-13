import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from page_loader.logger import get_logger

logger = get_logger(__name__)


def save_file(path, flag, data):
    try:
        file = open(path, flag)
    except OSError as error:
        logger.error(f'Error occured: {error}! Work stopped!')
    else:
        file.write(data)
        file.close()
        logger.info(f'File {path} successfully downloaded!')



def get_line_url_and_tag(line):
    if line.name == 'img':
        return line.get('src'), line.name
    elif line.name == 'link':
        return line.get('href'), line.name
    elif line.name == 'script' and line.get('src'):
        return line.get('src'), line.name
    else:
        return None, None


def get_line_data(obj_url, tag):

    try:
        response = requests.get(obj_url)
        response.raise_for_status()
    except HTTPError as http_error:
        logger.error(f'HTTP error occurred with inner resource: {http_error}! Work stopped!')
    except Exception as error:
        logger.error(f'Error occured with inner resource: {error}! Work stopped!')

    if tag == 'img':
        return response.content
    else:
        raw_line_response = requests.get(obj_url)
        raw_line_response.encoding = 'utf-8'
        return BeautifulSoup(raw_line_response.text, 'html.parser').prettify()
