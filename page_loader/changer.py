import os


def change_path(resource_tag, tag_name, file_path):
    link_from_tag = {
        'img': 'src',
        'script': 'src',
        'link': 'href', }
    res_path = os.path.join(os.path.basename(os.path.dirname(file_path)),
                            os.path.basename(file_path))
    resource_tag[link_from_tag[tag_name]] = res_path
    return resource_tag
