from pathlib import PurePosixPath

from page_loader.namer import (make_absolute_url, make_dir_name,
                               make_file_name, make_path, remove_schema)

MAIN_URL = 'https://page-loader.hexlet.repl.co'
EXPECTED_FILE_NAME = 'page-loader-hexlet-repl.co.html'
EXPECTED_DIR_NAME = 'page-loader-hexlet-repl-co_files'

PAGE_URL = 'https://page-loader.hexlet.repl.co/courses'
EXPECTED_HTML_NAME = 'page-loader-hexlet-repl-co-courses.html'

PNG_URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
EXPECTED_PNG_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'


def test_make_name():
    assert make_file_name(PAGE_URL) == EXPECTED_HTML_NAME
    assert make_file_name(PNG_URL) == EXPECTED_PNG_NAME
    assert make_file_name(MAIN_URL, True) == EXPECTED_FILE_NAME


def test_make_base_name():
    assert make_dir_name(MAIN_URL) == EXPECTED_DIR_NAME


def test_make_absolute_url():
    assert make_absolute_url('https://site.com/files',
                             'https://site.com/files/images/img.jpeg'
                             ) == 'https://site.com/files/images/img.jpeg'

    assert make_absolute_url('https://site.com/files',
                             'files/images/img.jpeg'
                             ) == 'https://site.com/files/images/img.jpeg'


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'


def test_make_path():
    PATH = 'dir/'
    MAIN_NAME = 'ru-hexlet-io-courses.co.html'
    EXPECTED = 'dir/ru-hexlet-io-courses.co.html'
    assert make_path(PATH, MAIN_NAME) == PurePosixPath(EXPECTED)
