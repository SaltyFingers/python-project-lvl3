import bs4
import requests_mock
from page_loader.web_manager import get_response, is_any_resources, make_soup

RAW_HTML_FILE = 'tests/fixtures/raw_html.html'

URL = 'https://page-loader.hexlet.repl.co'

FILES_PATH = 'tests/fixtures/for_mocker/'


@requests_mock.Mocker(kw='mock')
def test_get_and_parse_data(**kwargs):
    mock = kwargs['mock']
    mock.get(URL,
             text=open(RAW_HTML_FILE, 'r').read())
    assert type(make_soup(get_response(
                URL))) == bs4.BeautifulSoup


@requests_mock.Mocker(kw='mock')
def test_is_any_resources(**kwargs):
    mock = kwargs['mock']
    mock.get(URL, text=open(RAW_HTML_FILE, 'r').read())
    page_data = make_soup(get_response(URL))
    resources = page_data.find_all(['img', 'link', 'script'])
    assert is_any_resources(URL, resources) is True
