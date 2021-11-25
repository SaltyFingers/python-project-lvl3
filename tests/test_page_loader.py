from page_loader.loader import download, get_file_name, remove_schema
from unittest.mock import Mock


def test_download():
    mock = Mock()
    expect = '/home/soleny/python-project-lvl3/tmp/ru-hexlet-io-courses.html'
    assert download('https://ru.hexlet.io/courses', '/tmp') == expect


def test_get_file_name():
    expect = 'ru-hexlet-io-courses.html'
    assert get_file_name('https://ru.hexlet.io/courses') == expect


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
