import os

import pytest
from bs4 import BeautifulSoup
from page_loader.changer import change_path
from page_loader.namer import (make_absolute_url, make_name, make_path,
                               remove_schema)

# Data to test function which changes links to paths in .html file
ROOT_PATH = '/home/user/tmp/page-loader-hexlet-repl_files/'
LINE_1 = 'tests/fixtures/change_lines/line_1.html'
LINE_2 = 'tests/fixtures/change_lines/line_2.html'
LINE_3 = 'tests/fixtures/change_lines/line_3.html'
EXPECTED_1 = open('tests/fixtures/change_lines/expected_1.html', 'r').read()
EXPECTED_2 = open('tests/fixtures/change_lines/expected_2.html', 'r').read()
EXPECTED_3 = open('tests/fixtures/change_lines/expected_3.html', 'r').read()
PATH_1 = (os.path.join(ROOT_PATH,
          'page-loader-hexlet-repl-co-assets-application.css'))
PATH_2 = (os.path.join(
          ROOT_PATH,
          'page-loader-hexlet-repl-co-assets-professions-nodejs.png'))
PATH_3 = os.path.join(ROOT_PATH, 'page-loader-hexlet-repl-co-script.js')
# # # # #

MAIN_URL = 'https://page-loader.hexlet.repl.co'
EXPECTED_FILE_NAME = 'page-loader-hexlet-repl.co.html'
EXPECTED_DIR_NAME = 'page-loader-hexlet-repl-co_files'

PAGE_URL = 'https://page-loader.hexlet.repl.co/courses'
EXPECTED_HTML_NAME = 'page-loader-hexlet-repl-co-courses.html'

PNG_URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
EXPECTED_PNG_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'


def test_make_name_from_url():
    assert make_name(MAIN_URL, 'file') == EXPECTED_FILE_NAME
    assert make_name(MAIN_URL, 'dir') == EXPECTED_DIR_NAME
    assert make_name(PAGE_URL) == EXPECTED_HTML_NAME
    assert make_name(PNG_URL) == EXPECTED_PNG_NAME


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


def test_make_names():
    PATH = 'dir/'
    MAIN_NAME = 'ru-hexlet-io-courses.co.html'
    EXPECTED = 'dir/ru-hexlet-io-courses.co.html'
    assert make_path(PATH, MAIN_NAME) == EXPECTED


@pytest.mark.parametrize('line, tag, file_path, expected', [
    (LINE_1, 'link', PATH_1, EXPECTED_1),
    (LINE_2, 'img', PATH_2, EXPECTED_2),
    (LINE_3, 'script', PATH_3, EXPECTED_3), ])
def test_change_path(line, tag, file_path, expected):
    with open(line) as file:
        soup = BeautifulSoup(file, 'html.parser')
        res = soup.find(tag)
        assert str(change_path(res, tag, file_path)) == expected
