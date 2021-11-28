from pathlib import PurePosixPath
import pathlib
from urllib.parse import urlparse
import os
import requests
from bs4 import BeautifulSoup
from requests.models import Response


DIR_PATH = os.getcwd()


def download(url, path=DIR_PATH):
    changed_name = make_name_from_url(url)
    
    if path != DIR_PATH:
        working_dir = os.path.join(DIR_PATH, 
                                   PurePosixPath(path).relative_to('/'))
    else:
        working_dir = path

    names = {"main_dir": ''.join([changed_name, '.html']),
             "files_dir": ''.join([changed_name, '_files']),
    }

    path_to_file = os.path.join(working_dir, names['main_dir'])
    files_dir = os.path.join(working_dir, names['files_dir'])
    
    if os.path.exists(files_dir):
        pass
    else:
        os.mkdir(files_dir)
    
    raw_response = requests.get(url)
    raw_response.encoding = 'utf-8'

    with open(path_to_file, 'w+') as file:
        response = BeautifulSoup(raw_response.text, 'html.parser')
        file.write(response.prettify())

    images = get_image_from_html(path_to_file)\
    
    for image in images:
        print(image)
        image_name = os.path.join(files_dir, make_img_name(image))
        img_ = requests.get(image)
        with open(image_name, 'ab') as img_file:
            img_file.write(img_.content)
        
        with open(path_to_file, 'r+') as file:
            soup = BeautifulSoup(file, 'html.parser')
            line = soup.find(src=image)
            line.src = image_name
            file.write(str(line))
    
    return str(path_to_file)


def remove_schema(url):
    parsed_url = urlparse(url)
    scheme = '%s://' % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def make_name_from_url(url):
    page_name = []
    for s in remove_schema(url):
        if not s.isalnum():
            page_name.append('-')
        else:
            page_name.append(s)
    return ''.join(page_name)


def make_img_name(image):
    new_name = []
    suffix = pathlib.PurePosixPath(image).suffix
    for s in remove_schema(image)[:-len(suffix)]:
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append(suffix)
    return ''.join(new_name)


def get_image_from_html(path):
    images = []
    with open(path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for line in soup.find_all('img'):
            if line.get('itemprop') == "image":
                images.append(line.get('src'))
    return images