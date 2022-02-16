import argparse
import sys

from requests.exceptions import (ConnectionError, ConnectTimeout, HTTPError,
                                 SSLError)

from page_loader.loader import ROOT_DIR_PATH, download
from page_loader.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', help='page to download')
    parser.add_argument('-o',
                        '--output',
                        help='output folder',
                        default=ROOT_DIR_PATH)
    args = parser.parse_args()

    try:
        print(f'Starting download resources into {args.output}')
        download(args.url, args.output)
    except FileNotFoundError:
        print('Output or files directory does not exist! Can\'t save files!')
        sys.exit(1)
    except PermissionError:
        print('You don\'t have permission!')
        sys.exit(1)
    except SSLError:
        print('SSL error occurred!')
        sys.exit(1)
    except HTTPError:
        print('HTTP error occurred!')
        sys.exit(1)
    except ConnectTimeout:
        print('Connection timeout!')
        sys.exit(1)
    except ConnectionError:
        print('Connection error occured!')
        sys.exit(1)
    except OSError:
        print('Couldn\'t create a directory for files!')
        sys.exit(1)
    except Exception:
        print('Unexpexted error occured!')
        sys.exit(1)
    print(f'{args.url} successfully downloaded to {args.output}!')
    sys.exit(0)


if __name__ == '__main__':
    main()
