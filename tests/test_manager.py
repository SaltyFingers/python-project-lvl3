import imghdr
import os
import shutil
import stat
import tempfile

import bs4
import pytest
import requests
from page_loader.manager import (create_dir_for_files, get_data,
                                 is_any_resources, save_file)


@pytest.fixture
def tmp_dir():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)


def test_crete_dir_for_files(tmp_dir):
    path = os.path.join(tmp_dir, 'tmp_dir_files')
    create_dir_for_files(path)
    assert os.path.isdir(path)

    os.chmod(tmp_dir, stat.S_IRUSR)
    with pytest.raises(PermissionError) as e:
        create_dir_for_files(path)
    assert str(e.value) == 'You don\'t have permission!'
    os.chmod(tmp_dir, stat.S_IRWXU)


def test_get_data():
    IMG_PATH = 'https://page-loader.hexlet.repl.co\
/assets/professions/nodejs.png'
    assert type(get_data(
                'https://page-loader.hexlet.repl.co/')) == bs4.BeautifulSoup
    assert type(get_data(
                IMG_PATH, 'img')) == bytes


def test_is_any_resources():
    URL = 'https://page-loader.hexlet.repl.co/'
    page_data = get_data(URL)
    resources = page_data.find_all(['img', 'link', 'script'])
    assert is_any_resources(URL, resources) is True


def test_save_file(tmp_dir):
    DATA = 'hi, im data!'
    path = os.path.join(tmp_dir, 'file_name')
    save_file(path, 'w+', DATA)
    assert os.path.isfile(path)
    with open(path, 'r') as file:
        assert file.read() == 'hi, im data!'


def test_save_file_errors(tmp_dir):
    path = os.path.join(tmp_dir, 'file_name')

    with pytest.raises(FileNotFoundError) as e:
        save_file('dir/lol/path_to_file', 'w+', 'some_data')
    assert str(e.value) == 'Can\'t save file dir/lol/path_to_file!'

    os.chmod(tmp_dir, stat.S_IRUSR)

    with pytest.raises(PermissionError) as e:
        create_dir_for_files(path)
    assert str(e.value) == 'You don\'t have permission!'


def test_download_image(tmp_dir):
    NAME = 'nodejs.png'
    URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
    data = requests.get(URL).content
    path = os.path.join(tmp_dir, NAME)
    save_file(path, 'wb', data)
    assert os.path.exists(path)
    with open(path, 'rb') as img:
        content = img.read()
    assert content == data
    assert imghdr.what(path) == 'png'
