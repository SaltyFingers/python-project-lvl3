import os.path
import requests


def download(url, path):
    full_path = os.path.join(path, get_file_name(url))
    content = requests.get(url)
    with open(full_path, 'w') as file:
        file.write(content)
    return full_path


def get_file_name(url):
    if url.startswith('http'):
        name = url[8:]
    elif url.startswith('https'):
        name = url[9:]
    new_name = []
    for s in name:
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append('.html')
    return ''.join(new_name)
