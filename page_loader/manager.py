import requests
from bs4 import BeautifulSoup


def save_file(path, flag, data):
    with open(path, flag) as file:
        file.write(data)


def get_line_url_and_tag(line):
    if line.name == 'img':
        return line.get('src'), line.name
    elif line.name == 'link':
        return line.get('href'), line.name
    elif line.name == 'script' and line.get('src'):
        return line.get('src'), line.name
    else:
        return None, None


def get_line_data(obj_url, tag):
    if tag == 'img':
        return requests.get(obj_url).content
    else:
        raw_line_data = requests.get(obj_url)
        raw_line_data.encoding = 'utf-8'
        return BeautifulSoup(raw_line_data.text, 'html.parser').prettify()
