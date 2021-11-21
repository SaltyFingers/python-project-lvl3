from page_loader.page_loader import download, get_file_name
import requests
import requests_mock


def test_download():
    pass


def test_get_file_name():
    assert get_file_name('https://ru.hexlet.io/courses'
    ) == 'ru-hexlet-io-courses.html'