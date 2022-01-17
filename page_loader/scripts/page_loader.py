import argparse
import pathlib
import sys

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
        download(args.url, args.path)
    except Exception:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
