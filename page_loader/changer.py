import os


def make_new_line(line, tag, file_path):
    link_from_tag = {
        'img': 'src',
        'script': 'src',
        'link': 'href', }
    res_path = os.path.join(os.path.basename(os.path.dirname(file_path)),
                            os.path.basename(file_path))
    line[link_from_tag[tag]] = res_path
    return line
