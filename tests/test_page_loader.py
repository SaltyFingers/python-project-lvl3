from page_loader.loader import download, make_name_from_url, remove_schema
from unittest.mock import Mock
import os
import pyfakefs


# def test_download():
#     expect = '/home/soleny/python-project-lvl3/tmp/ru-hexlet-io-courses.html'
#     assert download('https://ru.hexlet.io/courses', '/tmp') == expect


# def test_create_files(fs):
#     path = os.path.join(os.getcwd(), '/lol')
#     fs.create_dir('/lol')
#     path = os.path.join(os.getcwd(), '/lol')
#     download('https://notepad-plus-plus.org/', '/lol')
#     assert os.path.exists('/lol/notepad-plus-plus-org.html')
#     assert os.path.exists('/lol/notepad-plus-plus-org_files/assets-images-notepad4ever.gif')
#     assert os.path.exists('/lol/notepad-plus-plus-org_files/notepad-plus-plus-org-images-logo.svg')
  



def test_make_name_from_url():
    assert make_name_from_url('https://ru.hexlet.io/courses') == 'ru-hexlet-io-courses'


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
