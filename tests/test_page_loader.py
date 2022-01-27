import imghdr
import os
import stat
import tempfile
from unittest.mock import Mock

import bs4
import requests
from page_loader.loader import download, is_any_resources
from page_loader.manager import create_dir_for_files, get_data, save_file

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'


def test_mock():
    mock = Mock()

    with tempfile.TemporaryDirectory() as tmp_dir:
        url = 'https://page-loader.hexlet.repl.co/'
        mock(download(url, tmp_dir))

        assert mock.call_count == 1


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
            assert SystemExit
        except SystemExit as e:
            assert str(e) == 'You don\'t have permission!'


def test_get_data():
    img_path = 'https://page-loader.hexlet.repl.co\
/assets/professions/nodejs.png'
    assert type(get_data(
                'https://page-loader.hexlet.repl.co/')) == bs4.BeautifulSoup
    assert type(get_data(
                img_path, 'img')) == bytes


def test_save_file():
    data = 'hi, im data!'

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        path = os.path.join(tmp_dir, 'file_name')
        save_file(path, 'w+', data)
        assert os.path.isfile(path)
        with open(path, 'r') as file:
            assert file.read() == 'hi, im data!'

        try:
            save_file('dir/lol/path_to_file', 'w+', data)
        except FileNotFoundError:
            assert SystemExit
        except SystemExit as e:
            assert str(e) == 'Directory does not exists!'

        try:
            os.chmod(tmp_dir, stat.S_IRUSR)
            save_file(path, 'w+', data)
        except PermissionError:
            assert SystemExit
        except SystemExit as e:
            assert str(e) == 'You don\'t have permission!'


def test_is_any_resources():
    url = 'https://page-loader.hexlet.repl.co/'
    page_data = get_data(url)
    resources = page_data.find_all(['img', 'link', 'script'])
    assert is_any_resources(url, resources) is True


def test_download_image():
    name = 'nodejs.png'
    url = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
    data = requests.get(url).content
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, name)
        save_file(path, 'wb', data)
        assert os.path.exists(path)
        with open(path, 'rb') as img:
            content = img.read()
        assert content == data
        assert imghdr.what(path) == 'png'


def test_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        url = 'https://page-loader.hexlet.repl.co/'
        download(url, tmp_dir)
        html_path = os.path.join(tmp_dir, 'page-loader-hexlet-repl.html')
        assert os.path.exists(html_path)

        path = os.path.join(tmp_dir, 'page-loader-hexlet-repl_files')
        assert os.path.isdir(path)
        assert len(os.listdir(path)) == 4


def test_no_permission_to_save_files():
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, stat.S_IRUSR)
        try:
            download('https://page-loader.hexlet.repl.co/', tmp_dir)
        except PermissionError:
            assert SystemExit
        except SystemExit as e:
            assert str(e) == 'You don\'t have permission!'


def test_wrong_url():
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            download('https://page-loader-which-not-exist.hexlet.repl.co/',
                     tmp_dir)
        except Exception as error:
            assert error
            assert SystemExit(1)
        except SystemExit as s_exit:
            assert (str(s_exit) == 'An error occured with \
                    https://page-loader-which-not-exist.hexlet.repl.co/')


def test_wrong_dir():
    try:
        download('https://page-loader.hexlet.repl.co/', '/not-exist/downloads')
    except FileNotFoundError as e:

        assert str(e) == 'Output directory does not exists!'
        assert SystemExit(1)
