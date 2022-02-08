import os

from page_loader.changer import make_main_name, make_path
from page_loader.logger import get_logger
from page_loader.manager import (check_output_dir, create_dir_for_files,
                                 download_resources, get_data,
                                 is_any_resources, save_file)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):
    check_output_dir(path)

    logger.info(f'Start downloading {url} to {path}')
    main_page_name = make_main_name(url, is_main=True)
    path_to_main_file = make_path(path, main_page_name, '.html')
    path_to_files_dir = make_path(path, main_page_name, '_files')
    page_data = get_data(url)
    resources = page_data.find_all(['img', 'link', 'script'])
    if is_any_resources(url, resources):
        create_dir_for_files(path_to_files_dir)
        print(f'Starting download resources into {path_to_files_dir}')
        logger.info(f'Starting download resources into {path_to_files_dir}')
        download_resources(url, page_data, path_to_files_dir)
    else:
        logger.info('No inner resources, saving file')
    processed_page_data = page_data.prettify()

    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, 'w', processed_page_data)
    print(f'Page downloaded into {path_to_main_file}')
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)
