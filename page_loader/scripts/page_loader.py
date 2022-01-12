import argparse
import pathlib
import sys

import requests
from requests.exceptions import HTTPError, SSLError

from page_loader.loader import download
from page_loader.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Page loader',
                                     conflict_handler='resolve')
    parser.add_argument('url')
    parser.add_argument('path', type=pathlib.Path)
    args = parser.parse_args()

    try:
        response = requests.get(args.url)
        response.raise_for_status()
    except SSLError as ssl_error:
        logger.error(f'SSL error occurred: {ssl_error}!')
        sys.exit(f'SSL error occurred with {args.url}')
    except HTTPError as http_error:
        logger.error(f'HTTP error occurred: {http_error}!')
        sys.exit(f'HTTP error occurred with {args.url}')
    except Exception as error:
        logger.error(f'An error occurred: {error}!')
        sys.exit(f'An error occurred with {args.url}')
    else:
        logger.info('Got response! Continue!')
        download(args.url, args.path)


if __name__ == '__main__':
    main()
