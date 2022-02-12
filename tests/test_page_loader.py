import os
import shutil
import stat
import tempfile
from http import HTTPStatus

import pytest
import requests_mock
from page_loader.loader import download
from requests.exceptions import ConnectionError, ConnectTimeout

TOTAL_FILES = 4

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'
EXPECTED_HTML_FILE = 'tests/fixtures/expected_html.html'

URL = 'https://page-loader.hexlet.repl.co'
CSS_URL = URL + '/assets/application.css'
COURSES_URL = URL + '/courses'
PNG_URL = URL + '/assets/professions/nodejs.png'
JS_URL = URL + '/script.js'

FILES_PATH = 'tests/fixtures/for_mocker/'
CSS_FILE = FILES_PATH + 'page-loader-hexlet-repl-co-assets-application.css'
PNG_FILE = (FILES_PATH + '\
page-loader-hexlet-repl-co-assets-professions-nodejs.png')
COURSES_FILE = FILES_PATH + 'page-loader-hexlet-repl-co-courses.html'
JS_FILE = FILES_PATH + 'page-loader-hexlet-repl-co-script.js'


@pytest.fixture
def tmp_dir():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)


@requests_mock.Mocker(kw='mock')
def test_mock_download(tmp_dir, **kwargs):
    mock = kwargs['mock']
    mock.get(URL,
             text=open(RAW_HTML_FILE, 'r').read())
    mock.get(CSS_URL,
             text=open(CSS_FILE, 'r').read())
    mock.get(COURSES_URL,
             text=open(COURSES_FILE, 'r').read())
    mock.get(PNG_URL,
             content=open(PNG_FILE, 'rb').read())
    mock.get(JS_URL,
             text=open(JS_FILE, 'r').read())

    download(URL, tmp_dir)
    html_path = os.path.join(tmp_dir, 'page-loader-hexlet-repl.html')
    assert os.path.exists(html_path)
    html_content = open(html_path, 'r').read()
    expected_content = open(EXPECTED_HTML_FILE, 'r').read()
    assert html_content == expected_content
    path = os.path.join(tmp_dir, 'page-loader-hexlet-repl_files')
    assert os.path.isdir(path)
    assert len(os.listdir(path)) == TOTAL_FILES


@requests_mock.Mocker(kw='mock')
def test_mock_dir_not_exists(tmp_dir, **kwargs):
    mock = kwargs['mock']
    path = os.path.join(tmp_dir, '/nope')
    mock.get(URL)
    with pytest.raises(FileNotFoundError) as e:
        download(URL, path)
    assert str(e.value) == 'Output directory does not exists!'
    assert not os.listdir(tmp_dir)


@requests_mock.Mocker(kw='mock')
def test_mock_wrong_url(tmp_dir, **kwargs):
    mock = kwargs['mock']
    mock.get(URL, status_code=HTTPStatus.NOT_FOUND)
    with pytest.raises(Exception) as e:
        download(URL, tmp_dir)
    assert str(e.value) == 'Responce code is not 200! It\'s: 404'
    assert not os.listdir(tmp_dir)


@requests_mock.Mocker(kw='mock')
def test_mock_no_permission(tmp_dir, **kwargs):
    mock = kwargs['mock']
    os.chmod(tmp_dir, stat.S_IRUSR)
    mock.get(URL)
    with pytest.raises(PermissionError) as e:
        download(URL, tmp_dir)
    assert str(e.value) == 'You don\'t have permission!'
    assert not os.listdir(tmp_dir)


@requests_mock.Mocker(kw='mock')
def test_mock_code_500(tmp_dir, **kwargs):
    mock = kwargs['mock']
    mock.get(URL, status_code=500)
    with pytest.raises(ConnectionError) as e:
        download(URL, tmp_dir)
    assert str(e.value) == 'Responce code is not 200! It\'s: 500'
    assert not os.listdir(tmp_dir)


@requests_mock.Mocker(kw='mock')
def test_mock_timeout(tmp_dir, **kwargs):
    mock = kwargs['mock']
    mock.get(URL, exc=ConnectTimeout)
    with pytest.raises(ConnectTimeout) as e:
        download(URL, tmp_dir)
    assert str(e.value) == 'Connection Timeout!'
    assert not os.listdir(tmp_dir)
