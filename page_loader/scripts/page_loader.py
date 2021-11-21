import argparse
import pathlib
from page_loader.page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Page loader',
                                     conflict_handler='resolve')
    parser.add_argument('url', type=str)
    parser.add_argument('path', type=pathlib.Path)
    args = parser.parse_args()
    download(args.url, args.path)


if __name__ == '__main__':
    main()
