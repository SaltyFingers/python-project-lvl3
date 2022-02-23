import bs4
import requests_mock
from page_loader.web_manager import get_response, is_any_resources, parse_data

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'

URL = 'https://page-loader.hexlet.repl.co'
PNG_URL = URL + '/assets/professions/nodejs.png'

FILES_PATH = 'tests/fixtures/for_mocker/'
PNG_FILE = (FILES_PATH + '\
page-loader-hexlet-repl-co-assets-professions-nodejs.png')


@requests_mock.Mocker(kw='mock')
def test_get_and_parse_data(**kwargs):
    mock = kwargs['mock']
    mock.get(URL,
             text=open(RAW_HTML_FILE, 'r').read())
    mock.get(PNG_URL,
             content=open(PNG_FILE, 'rb').read())
    assert type(parse_data(get_response(
                URL))) == bs4.BeautifulSoup
    assert type(parse_data(get_response(
                PNG_URL), 'img')) == bytes


@requests_mock.Mocker(kw='mock')
def test_is_any_resources(**kwargs):
    mock = kwargs['mock']
    mock.get(URL, text=open(RAW_HTML_FILE, 'r').read())
    page_data = parse_data(get_response(URL))
    resources = page_data.find_all(['img', 'link', 'script'])
    assert is_any_resources(URL, resources) is True
