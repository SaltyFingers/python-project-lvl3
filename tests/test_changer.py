import os

import pytest
from bs4 import BeautifulSoup
from page_loader.changer import (make_absolute_url, make_main_name,
                                 make_new_line, make_path, remove_schema)

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


def test_make_name_from_url():
    assert make_main_name('https://ru.hexlet.io/courses'
                          ) == 'ru-hexlet-io-courses.html'
    assert make_main_name('https://ru.hexlet.io/courses',
                          True) == 'ru-hexlet-io-courses'
    assert make_main_name('some/image/right.here'
                          ) == 'some-image-right.here'
    assert make_main_name('some/image/right.here',
                          True) == 'some-image-right'


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
    PATH = 'dir/dir'
    MAIN_NAME = 'ru-hexlet-io-courses'
    EXPECTED = 'dir/dir/ru-hexlet-io-courses.html'
    assert make_path(PATH, MAIN_NAME, '.html') == EXPECTED


@pytest.mark.parametrize('line, tag, file_path, expected', [
    (LINE_1, 'link', PATH_1, EXPECTED_1),
    (LINE_2, 'img', PATH_2, EXPECTED_2),
    (LINE_3, 'script', PATH_3, EXPECTED_3), ])
def test_make_new_line(line, tag, file_path, expected):
    with open(line) as file:
        soup = BeautifulSoup(file, 'html.parser')
        res = soup.find(tag)
        assert str(make_new_line(res, tag, file_path)) == expected
