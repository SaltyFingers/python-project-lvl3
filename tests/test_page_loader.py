import os
import stat
import tempfile
from unittest.mock import Mock

from page_loader.loader import download

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'
URL = 'https://page-loader.hexlet.repl.co/'


def test_mock():
    mock = Mock()

    with tempfile.TemporaryDirectory() as tmp_dir:
        mock(download(URL, tmp_dir))
        assert mock.call_count == 1


def test_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        download(URL, tmp_dir)
        html_path = os.path.join(tmp_dir, 'page-loader-hexlet-repl.html')
        assert os.path.exists(html_path)

        path = os.path.join(tmp_dir, 'page-loader-hexlet-repl_files')
        assert os.path.isdir(path)
        assert len(os.listdir(path)) == 4


def test_no_permission_to_save_files():
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, stat.S_IRUSR)
        try:
            download(URL, tmp_dir)
        except PermissionError:
            assert PermissionError
            assert SystemExit


def test_wrong_url():
    URL = 'https://page-loader-which-not-exist.hexlet.repl.co/'
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            download(URL, tmp_dir)
        except Exception:
            assert Exception
            assert SystemExit


def test_wrong_dir():
    try:
        download(URL, '/not-exist/downloads')
    except FileNotFoundError:
        assert FileNotFoundError
        assert SystemExit
