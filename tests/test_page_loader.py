# import os
# from os.path import exists
# from unittest.mock import Mock

# import pyfakefs
# import requests
# from page_loader.loader import (download, make_name_from_url, remove_schema,
#                                 save_image)

# # def test_download(tmpdir_factory):
# #     expect = '/home/soleny/python-project-lvl3/tmp/ru-hexlet-io-courses.html'
# #     assert download('https://ru.hexlet.io/courses', '/tmp') == expect


# def test_save_image(fs):
#     try:
#         fs.create_file('/tmp')
#     except FileExistsError:
#         pass
#     save_image('/tmp', 'https://notepad-plus-plus.org/images/logo.svg')
#     assert exists('/tmp/notepad-plus-plus-org-images-logo.svg')
#     save_image('/tmp', '/assets/images/notepad4ever.png')
#     assert exists('/tmp/assets-images-notepad4ever.png')


# def test_change_urls(fs):
#     try:
#         fs.create_file('/tmp')
#     except FileExistsError:
#         pass
#     try:
#         path = download('https://notepad-plus-plus.org/', '/tmp')
#     except FileNotFoundError:
#         pass
#     with open(path, 'r') as file:
#         data = file.read()
#     assert requests.get('https://notepad-plus-plus.org/').text != data



# def test_make_name_from_url():
#     assert make_name_from_url('https://ru.hexlet.io/courses') == 'ru-hexlet-io-courses'


# def tets_remove_schema():
#     assert remove_schema('https://site.com') == 'site.com'
#     assert remove_schema('http://site.com') == 'site.com'
#     assert remove_schema('site.com') == 'site.com'
