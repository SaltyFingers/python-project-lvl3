from page_loader.loader import download, get_file_name, remove_schema


def test_download():
    assert download('https://ru.hexlet.io/courses', '/tmp'
    ) == """/home/soleny/python-project-lvl3/tmp/ru-hexlet-io-courses.html"""  # noqa


def test_get_file_name():
    assert get_file_name('https://ru.hexlet.io/courses'
    ) == 'ru-hexlet-io-courses.html'  # noqa


def tets_remove_schema():
    assert remove_schema('https://site.com') == 'site.com'
    assert remove_schema('http://site.com') == 'site.com'
    assert remove_schema('site.com') == 'site.com'
