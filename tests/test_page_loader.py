import imghdr
import os
import stat
import tempfile

import requests
from bs4 import BeautifulSoup
from page_loader.changer import (make_absolute_url, make_name_from_url,
                                 remove_schema)
from page_loader.loader import change_url, download, save_file

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'


def test_save_file():
    data = 'hi, im data!'

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        save_file(path, 'w+', data)
        assert os.path.isfile(path)
        with open(path, 'r') as file:
            assert file.read() == 'hi, im data!'


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
        assert len(os.listdir(path)) ==  4

        with open(html_path, 'r') as file:
            new_data = file.read()
            raw_data = open(RAW_HTML_FILE).read()
            assert new_data != raw_data


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
            download('https://page-loader-which-not-exist.hexlet.repl.co/', tmp_dir)
        except Exception as error:
            assert error
            assert SystemExit
        except SystemExit as s_exit:
            assert str(s_exit) == 'Someting went wrong!'


def test_wrong_dir():
    try:
        download('https://page-loader.hexlet.repl.co/', '/not-exist/downloads')
    except SystemExit as e:
        assert str(e) == 'Output directory does not exist!'


def test_make_name_from_url():
    assert make_name_from_url('https://ru.hexlet.io/courses'
                              ) == 'ru-hexlet-io-courses.html'
    assert make_name_from_url('https://ru.hexlet.io/courses',
                              True) == 'ru-hexlet-io-courses'
    assert make_name_from_url('some/image/right.here'
                              ) == 'some-image-right.here'
    assert make_name_from_url('some/image/right.here',
                              True) == 'some-image-right'


def test_make_absolute_url():
    assert make_absolute_url('https://super-site.com/files',
                             'https://super-site.com/files/images/img.jpeg') == 'https://super-site.com/files/images/img.jpeg'
    assert make_absolute_url('https://super-site.com/files',
                             'files/images/img.jpeg') == 'https://super-site.com/files/images/img.jpeg'


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
