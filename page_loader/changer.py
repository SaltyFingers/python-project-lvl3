import os


def change_path(string, tag, file_path):
    link_from_tag = {
        'img': 'src',
        'script': 'src',
        'link': 'href', }
    res_path = os.path.join(os.path.basename(os.path.dirname(file_path)),
                            os.path.basename(file_path))
    string[link_from_tag[tag]] = res_path
    return string
