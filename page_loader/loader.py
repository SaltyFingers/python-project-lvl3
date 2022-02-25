import os

from page_loader.files_manager import (check_output_dir, create_dir_for_files,
                                       save_file)
from page_loader.logger import get_logger
from page_loader.namer import make_dir_name, make_file_name, make_path
from page_loader.web_manager import (download_resources, get_response,
                                     is_any_resources, make_soup)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):
    check_output_dir(path)

    logger.info(f'Start downloading {url} to {path}')
    path_to_output_file = make_path(path, make_file_name(url,
                                                         is_output_file=True))
    path_to_files_dir = make_path(path, make_dir_name(url))
    raw_response = get_response(url)
    soup = make_soup(raw_response)
    resources = soup.find_all(['img', 'link', 'script'])
    if is_any_resources(url, resources):
        create_dir_for_files(path_to_files_dir)
        logger.info(f'Starting download resources into {path_to_files_dir}')
        download_resources(url, soup, path_to_files_dir)
    else:
        logger.info('No inner resources, saving file')
    logger.info(f'Saving {path_to_output_file}!')
    save_file(path_to_output_file, soup.prettify())
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_output_file)
