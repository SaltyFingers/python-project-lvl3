import os

from page_loader.logger import get_logger

logger = get_logger(__name__)


def create_dir_for_files(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except PermissionError as error:
        logger.error(f'Permission error: {error}')
        raise PermissionError('You don\'t have permission!')

    except OSError as e:
        logger.error(f'Another error occured: {e}')
        raise OSError('Couldn\'t create a directory for files!')


def save_file(path, data):
    flag = 'wb' if is_bytes(data) else 'w'
    try:
        with open(path, flag) as file:
            file.write(data)

    except PermissionError as error:
        logger.error(f'Permission error occured: {error}!')
        raise PermissionError('You don\'t have permission!')

    except FileNotFoundError as error:
        logger.error(f'Can\'t save file {path}! Error: {error}')
        raise FileNotFoundError(f'Can\'t save file {path}!')


def check_output_dir(path):
    if not os.path.exists(path):
        logger.error(f'Output directory {path} does not exist!')
        raise FileNotFoundError('Output directory does not exists!')


def is_bytes(data):
    return isinstance(data, bytes)
