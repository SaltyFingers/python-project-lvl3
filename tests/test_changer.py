from pathlib import PurePath

import pytest
from bs4 import BeautifulSoup
from page_loader.changer import change_path


ROOT_PATH = '/home/user/tmp/page-loader-hexlet-repl_files/'
LINE_1 = 'tests/fixtures/change_lines/line_1.html'
LINE_2 = 'tests/fixtures/change_lines/line_2.html'
LINE_3 = 'tests/fixtures/change_lines/line_3.html'
EXPECTED_1 = open('tests/fixtures/change_lines/expected_1.html', 'r').read()
EXPECTED_2 = open('tests/fixtures/change_lines/expected_2.html', 'r').read()
EXPECTED_3 = open('tests/fixtures/change_lines/expected_3.html', 'r').read()
PATH_1 = (PurePath(ROOT_PATH,
          'page-loader-hexlet-repl-co-assets-application.css'))
PATH_2 = (PurePath(ROOT_PATH,
          'page-loader-hexlet-repl-co-assets-professions-nodejs.png'))
PATH_3 = PurePath(ROOT_PATH, 'page-loader-hexlet-repl-co-script.js')


@pytest.mark.parametrize('line, tag, file_path, expected', [
    (LINE_1, 'link', PATH_1, EXPECTED_1),
    (LINE_2, 'img', PATH_2, EXPECTED_2),
    (LINE_3, 'script', PATH_3, EXPECTED_3), ])
def test_change_path(line, tag, file_path, expected):
    with open(line) as file:
        soup = BeautifulSoup(file, 'html.parser')
        res = soup.find(tag)
        assert str(change_path(res, tag, file_path)) == expected
