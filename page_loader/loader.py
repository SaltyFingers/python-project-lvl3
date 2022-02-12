import os

from page_loader.files_manager import (check_output_dir, create_dir_for_files,
                                       save_file)
from page_loader.logger import get_logger
from page_loader.namer import make_name, make_path
from page_loader.web_manager import (download_resources, get_data,
                                     is_any_resources, parse_data)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):
    check_output_dir(path)

    logger.info(f'Start downloading {url} to {path}')
    original_page_name = make_name(url, only_name=True)
    path_to_main_file = make_path(path, original_page_name, '.html')
    path_to_files_dir = make_path(path, original_page_name, '_files')
    raw_data = get_data(url)
    parsed_data = parse_data(raw_data)
    resources = parsed_data.find_all(['img', 'link', 'script'])
    if is_any_resources(url, resources):
        create_dir_for_files(path_to_files_dir)
        logger.info(f'Starting download resources into {path_to_files_dir}')
        download_resources(url, parsed_data, path_to_files_dir)
    else:
        logger.info('No inner resources, saving file')
    processed_page_data = parsed_data.prettify()

    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, processed_page_data)
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)
