import os
import tempfile
from os.path import exists
import pathlib
from page_loader.changer import (make_absolute_url, make_name_from_url,
                                 remove_schema)
from page_loader.loader import download, save_file, change_url


def test_save_file():
    data = 'hi, im data!'
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        save_file(path, 'w+', data)
        assert os.path.isfile(path)
        with open(path, 'r') as file:
            assert file.read() == 'hi, im data!'


def test_make_name_from_url():
    assert make_name_from_url('https://ru.hexlet.io/courses') == 'ru-hexlet-io-courses.html'
    assert make_name_from_url('https://ru.hexlet.io/courses', True) == 'ru-hexlet-io-courses'
    assert make_name_from_url('some/image/right.here') == 'some-image-right.here'
    assert make_name_from_url('some/image/right.here', True) == 'some-image-right'


def test_make_absolute_url():
    assert make_absolute_url('https://super-site.com/files',
                             'https://super-site.com/files/images/img.jpeg') == 'https://super-site.com/files/images/img.jpeg'
    assert make_absolute_url('https://super-site.com/files',
                             'files/images/img.jpeg') == 'https://super-site.com/files/images/img.jpeg'


def test_change_url():
    pass


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
