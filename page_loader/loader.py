import os

from page_loader.changer import make_main_name, make_path
from page_loader.logger import get_logger
from page_loader.manager import (get_data, is_directory_exists, process_data,
                                 save_file)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path):
    is_directory_exists(path)
    if path == 'current':
        path = ROOT_DIR_PATH

    logger.info(f'Start downloading {url} to {path}')
    main_page_name = make_main_name(url, is_main=True)
    path_to_main_file = make_path(path, main_page_name, '.html')
    path_to_files_dir = make_path(path, main_page_name, '_files')
    processed_page_data = process_data(get_data(url), url, path_to_files_dir)
    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, 'w', processed_page_data.prettify())
    print(f'Page downloaded into {path_to_main_file}')
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)
