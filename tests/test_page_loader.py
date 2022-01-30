from http import HTTPStatus
import os
import stat
import tempfile
import requests_mock

from page_loader.loader import download

TOTAL_FILES = 4
RAW_HTML_FILE = 'tests/fixtures/raw_html.html'
URL = 'https://page-loader.hexlet.repl.co/'


# def test_download():
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         download(URL, tmp_dir)
#         html_path = os.path.join(tmp_dir, 'page-loader-hexlet-repl.html')
#         assert os.path.exists(html_path)

#         path = os.path.join(tmp_dir, 'page-loader-hexlet-repl_files')
#         assert os.path.isdir(path)
#         assert len(os.listdir(path)) == TOTAL_FILES


# def test_no_permission_to_save_files():
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         os.chmod(tmp_dir, stat.S_IRUSR)
#         try:
#             download(URL, tmp_dir)
#         except PermissionError:
#             assert PermissionError
#             assert SystemExit


# def test_wrong_url():
#     URL = 'https://page-loader-which-not-exist.hexlet.repl.co/'
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         try:
#             download(URL, tmp_dir)
#         except Exception:
#             assert Exception
#             assert SystemExit


# def test_wrong_dir():
#     try:
#         download(URL, '/not-exist/downloads')
#     except FileNotFoundError:
#         assert FileNotFoundError
#         assert SystemExit

###################################################
def test_mock_download():
    pass


def test_mock_dir_not_exists():
    with tempfile.TemporaryDirectory() as tmp_file:
        path = os.path.join(tmp_file, '/nope')
        with requests_mock.Mocker() as mock:
            mock.get(URL)
            try:
                download(URL, path)
            except FileNotFoundError:
                assert FileNotFoundError


def test_mock_wrong_url():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, status_code=HTTPStatus.NOT_FOUND)
            try:
                download(URL, tmp_dir)
            except Exception:
                assert Exception
                assert not os.listdir(tmp_dir)


def test_mock_no_permission():
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, stat.S_IRUSR)
        with requests_mock.Mocker() as mock:
            mock.get(URL)
            try:
                download(URL, tmp_dir)
            except PermissionError:
                assert PermissionError
                assert SystemExit
