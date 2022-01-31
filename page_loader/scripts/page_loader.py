import argparse
import sys

from page_loader.loader import download
from page_loader.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', help='page to download')
    parser.add_argument('-o',
                        '--output',
                        help='output folder',
                        default='current')
    args = parser.parse_args()

    try:
        download(args.url, args.output)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
