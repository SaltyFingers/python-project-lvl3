import argparse
import os
import pathlib

import requests
from requests.exceptions import HTTPError

from page_loader.loader import download
from page_loader.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Page loader',
                                     conflict_handler='resolve')
    parser.add_argument('url')
    parser.add_argument('path', type=pathlib.Path, default=os.getcwd())
    args = parser.parse_args()

    try:
        requests.get(args.url).raise_for_status()
    except HTTPError as http_error:
        logger.error(f'HTTP error occurred: {http_error}! Work stopped!')
    except Exception as error:
        logger.error(f'Error occured: {error}! Work stopped!')
    else:
        logger.info('Got response! Continue!')
        download(args.url, args.path)


if __name__ == '__main__':
    main()
