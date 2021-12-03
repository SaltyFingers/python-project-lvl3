import os
from pathlib import PurePosixPath
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.changer import (make_correct_url,
                                 make_name_from_url)

DIR_PATH = os.getcwd()

 

def download(url, path=DIR_PATH):
    if path != DIR_PATH:
        working_dir = os.path.join(DIR_PATH,
                                   PurePosixPath(path).relative_to('/'))
    else:
        working_dir = path

    names = {"main_dir": ''.join([make_name_from_url(url, is_main=True), '.html']),
             "files_dir": ''.join([make_name_from_url(url, is_main=True), '_files']), }

    path_to_file = os.path.join(working_dir, names['main_dir'])
    files_dir_path = os.path.join(working_dir, names['files_dir'])

    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)

    raw_data = requests.get(url)
    raw_data.encoding = 'utf-8'

    with open(path_to_file, 'w+') as file:
        data = BeautifulSoup(raw_data.text, 'html.parser')
        
        # DOWNLOAD IMAGES
        for line in data.find_all('img'):
            img_url = line.get('src')
            img_name = make_name_from_url(img_url)
            line['src'] = os.path.join(files_dir_path, img_name)
            save_image(make_correct_url(url, img_url), 
                       img_name, files_dir_path)

        main_host = urlparse(url).netloc

        # DOWNLOAD LINKS
        for line in data.find_all('link'):
            link_url = line.get('href')
            link_host = urlparse(link_url).netloc
            if (link_host == main_host or not link_host) and link_url != url:
                link_name = make_name_from_url(link_url)
                path = os.path.join(files_dir_path, link_name)
                raw_link_data = requests.get(make_correct_url(url, link_url))
                raw_link_data.encoding = 'utf-8'
                link_data = BeautifulSoup(raw_link_data.text, 'html.parser')
                line['href'] = path
                with open(path, 'w+') as link_file:
                    link_file.write(link_data.prettify())
        
        # DOWNLOAD SCRIPTS
        for line in data.find_all('script'):
            if line.get('scr'):
                script_url = line.get('scr')
            else:
                continue
            script_host = urlparse(script_url).netloc
            if (script_host == main_host or not script_host) and script_url != url:
                script_name = make_name_from_url(script_url)
                path = os.path.join(files_dir_path, script_name)
                raw_script_data = requests.get(make_correct_url(url, script_url))
                raw_script_data.encoding = 'utf-8'
                script_data = BeautifulSoup(raw_script_data.text, 'html.parser')
                line['scr'] = path
                with open(path, 'w+') as script_file:
                    script_file.write(script_data.prettify())

        file.write(data.prettify())
    return str(path_to_file)

def save_image(img_url, img_name, files_dir_path):
    path_to_image = os.path.join(files_dir_path, img_name)
    with open(path_to_image, 'ab') as image:
        image.write(requests.get(img_url).content)
