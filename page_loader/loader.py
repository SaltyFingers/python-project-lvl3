import os
import sys
from urllib.parse import urlparse

from progress.bar import Bar

from page_loader.changer import (change_url, make_absolute_url,
                                 make_name_from_url)
from page_loader.logger import get_logger
from page_loader.manager import (create_dir_for_files, get_data,
                                 get_line_url_and_tag,
                                 save_file)

ROOT_DIR_PATH = os.getcwd()
logger = get_logger(__name__)


def download(url, path=ROOT_DIR_PATH):
    if not os.path.exists(path):
        logger.error(f'Output directory {path} does not exist!')
        sys.exit('Output directory does not exist!')
    logger.info(f'Start downloading {url} to {path}')
    main_page_name = make_name_from_url(url, is_main=True)
    path_to_main_file = os.path.join(path, main_page_name + '.html')
    path_to_files_dir = os.path.join(path, main_page_name + '_files')
    page_data = get_data(url)
    resources = page_data.find_all(['img', 'link', 'script'])
    if is_any_resources(url, resources):
        create_dir_for_files(path_to_files_dir)
        print(f'Starting download resources into {path_to_files_dir}')
        download_resources(url, page_data, path_to_files_dir)
    else:
        logger.info('No inner resources, saving file')
    logger.info(f'Saving {path_to_main_file}!')
    save_file(path_to_main_file, 'w+', page_data.prettify())
    print(f'Page downloaded into {path_to_main_file}')
    logger.info(f'{url} successfully downloaded!')
    return str(path_to_main_file)


def is_any_resources(url, resources):
    is_iner_res_bool_list = []
    for line in resources:
        line_url = get_line_url_and_tag(line)[1]
        is_iner_res_bool_list.append(is_proper_to_download(url, line_url))
    return any(is_iner_res_bool_list)


def is_proper_to_download(url, line_url):
    main_host = urlparse(url).netloc
    line_url_host = urlparse(line_url).netloc
    return (line_url or line_url != url or (
            line_url_host and line_url_host == main_host))


def download_resources(url, data, path_to_files_dir):
    bar = Bar('Downloading resouces ',
              max=len(data.find_all(['img', 'link', 'script'])))
    for line in data.find_all(['img', 'link', 'script']):
        line_url, tag = get_line_url_and_tag(line)
        absolute_url = make_absolute_url(url, line_url)
        if not is_proper_to_download(url, line_url):
            bar.next()
            continue
        file_name = make_name_from_url(line_url)
        file_path = os.path.join(path_to_files_dir, file_name)
        logger.info(f'Downloading {absolute_url}')
        line_data = get_data(absolute_url, tag)
        flag = 'wb' if tag == 'img' else 'w+'
        save_file(file_path, flag, line_data)
        logger.info('File successfully downloaded!')
        line = change_url(line, tag, file_path)
        bar.next()
    bar.finish()
