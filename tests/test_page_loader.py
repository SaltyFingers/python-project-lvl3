import os
import pathlib
import tempfile
from os.path import exists

import requests
from bs4 import BeautifulSoup
from page_loader.changer import (make_absolute_url, make_name_from_url,
                                 remove_schema)
from page_loader.loader import change_url, download, save_file
from requests import exceptions
from requests.exceptions import HTTPError, SSLError


def test_save_file():
    data = 'hi, im data!'
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, 'file_name')
        save_file(path, 'w+', data)
        assert os.path.isfile(path)
        with open(path, 'r') as file:
            assert file.read() == 'hi, im data!'


def test_download():
    with tempfile.TemporaryDirectory() as tmp_dir:
        url = 'https://page-loader.hexlet.repl.co/'
        # os.mkdir(os.path.join(tmp_dir, 'page-loader-hexlet-repl_files'))
        download(url, tmp_dir)
        html_path = os.path.join(tmp_dir, 'page-loader-hexlet-repl.html')
        assert os.path.exists(html_path)
        
        path = os.path.join(tmp_dir, 'page-loader-hexlet-repl_files')
        assert len(os.listdir(path)) ==  4
        
        with open(html_path, 'r') as file:
            new_data = file.read()
            raw_data = requests.get(url)
            old_data = BeautifulSoup(raw_data.text, 'html.parser')
            assert new_data != old_data



def test_wrong_url():
    with tempfile.TemporaryDirectory() as tmp_dir:   
        try:
            download('https://page-loader-which-not-exist.hexlet.repl.co/', tmp_dir)
        except SSLError as error:
            assert error
            assert SystemExit
        except SystemExit as s_exit:
            assert str(s_exit) == 'SSL error occurred!'



def test_wrong_dir():
    try:
        download('https://page-loader.hexlet.repl.co/', '/not-exist/downloads')
    except SystemExit as e:
        assert str(e) == 'Output directory does not exist!'


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


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
