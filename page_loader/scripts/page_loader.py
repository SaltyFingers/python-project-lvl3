import argparse
import os
import pathlib

from page_loader.loader import download


def main():
    parser = argparse.ArgumentParser(description='Page loader',
                                     conflict_handler='resolve')
    parser.add_argument('url')
    parser.add_argument('path', type=pathlib.Path, default=os.getcwd())
    args = parser.parse_args()
    download(args.url, args.path)


if __name__ == '__main__':
    main()
