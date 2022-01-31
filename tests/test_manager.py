import imghdr
import os
import stat
import tempfile

import bs4
import requests
from page_loader.manager import (create_dir_for_files, get_data,
                                 is_any_resources, save_file, process_data)


def test_crete_dir_for_files():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'tmp_dir_files')
        create_dir_for_files(path)
        assert os.path.isdir(path)

        try:
            create_dir_for_files(path)
        except FileExistsError:
            assert FileExistsError
        os.chmod(path, stat.S_IRUSR)
        try:
            create_dir_for_files(path)
        except PermissionError:
            assert PermissionError


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


def test_save_file():
    DATA = 'hi, im data!'
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        save_file(path, 'w+', DATA)
        assert os.path.isfile(path)
        with open(path, 'r') as file:
            assert file.read() == 'hi, im data!'


def test_save_file_errors():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        try:
            save_file('dir/lol/path_to_file', 'w+', 'some_data')
        except FileNotFoundError:
            assert FileNotFoundError

        try:
            os.chmod(tmp_dir, stat.S_IRUSR)
            save_file(path, 'w+', 'some_data')
        except PermissionError:
            assert PermissionError


def test_download_image():
    NAME = 'nodejs.png'
    URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
    data = requests.get(URL).content
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, NAME)
        save_file(path, 'wb', data)
        assert os.path.exists(path)
        with open(path, 'rb') as img:
            content = img.read()
        assert content == data
        assert imghdr.what(path) == 'png'


def test_process():
    url = 'https://page-loader.hexlet.repl.co/'
    dir = '/page-loader-hexlet-repl_files'
    raw_html = bs4.BeautifulSoup(open('tests/fixtures/raw_html.html',
                                      'r').read(), 'html.parser')
    expected_html = open('tests/fixtures/expected_html.html', 'r').read()

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = tmp_dir + dir
        processed_html = process_data(raw_html, url, path)

    assert processed_html == expected_html
