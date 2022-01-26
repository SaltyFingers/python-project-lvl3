import pytest
import os
import bs4
from bs4 import BeautifulSoup
from page_loader.changer import (make_absolute_url, make_main_name,
                                 make_new_line, make_path, remove_schema)
ROOT_PATH = '/home/user/tmp/page-loader-hexlet-repl_files/'
LINE_1 = BeautifulSoup(open('tests/fixtures/change_lines/line_1.html', 'rb'
                            ).read(), 'html.parser')
EXPECTED_1 = BeautifulSoup(open('tests/fixtures/change_lines/expected_1.html', 'rb'
                                ).read(), 'html.parser')
PATH_1 = os.path.join(ROOT_PATH, 'page-loader-hexlet-repl-co-assets-application.css')
# LINK_2 = '/assets/professions/nodejs.png'
# EXPECTED_2 = '''
# page-loader-hexlet-repl_files/
# page-loader-hexlet-repl-co-assets-professions-nodejs.png
# '''
# LINK_3 = '/script.js'
# EXPECTED_3 = '''
# page-loader-hexlet-repl_files/
# page-loader-hexlet-repl-co-script.js
# '''


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

@pytest.mark.parametrize('line, tag, file_path, expected' ,[
    (LINE_1, 'link', PATH_1, EXPECTED_1),
    # (LINK_2, 'img', PATH, EXPECTED_2),
    # (LINK_2, 'script', PATH, EXPECTED_2), 
    ])
def test_make_new_line(line, tag, file_path, expected):
    assert str(make_new_line(line, tag, file_path)) == str(expected)
