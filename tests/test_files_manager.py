import imghdr
import os
import shutil
import stat
import tempfile

import pytest
import requests
import requests_mock
from page_loader.files_manager import create_dir_for_files, save_file

URL = 'https://page-loader.hexlet.repl.co'
PNG_URL = URL + '/assets/professions/nodejs.png'

FILES_PATH = 'tests/fixtures/for_mocker/'
PNG_FILE = (FILES_PATH + '\
page-loader-hexlet-repl-co-assets-professions-nodejs.png')


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


def test_save_file(tmp_dir):
    DATA = 'hi, im data!'
    path = os.path.join(tmp_dir, 'file_name')
    save_file(path, DATA)
    assert os.path.isfile(path)
    with open(path, 'r') as file:
        assert file.read() == 'hi, im data!'


def test_save_file_errors(tmp_dir):
    path = os.path.join(tmp_dir, 'file_name')

    with pytest.raises(FileNotFoundError) as e:
        save_file('dir/lol/path_to_file', 'some_data')
    assert str(e.value) == 'Can\'t save file dir/lol/path_to_file!'

    os.chmod(tmp_dir, stat.S_IRUSR)

    with pytest.raises(PermissionError) as e:
        create_dir_for_files(path)
    assert str(e.value) == 'You don\'t have permission!'


@requests_mock.Mocker(kw='mock')
def test_download_image(tmp_dir, **kwargs):
    mock = kwargs['mock']
    mock.get(PNG_URL,
             content=open(PNG_FILE, 'rb').read())
    data = requests.get(PNG_URL).content
    path = os.path.join(tmp_dir, 'nodejs.png')
    save_file(path, data)
    assert os.path.exists(path)
    with open(path, 'rb') as img:
        content = img.read()
    assert content == data
    assert imghdr.what(path) == 'png'
