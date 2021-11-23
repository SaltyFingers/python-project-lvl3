from pathlib import Path, PurePosixPath


def download(url, path):
    DIR_PATH = Path.cwd()
    path_to_file = Path(DIR_PATH, PurePosixPath(path).relative_to('/'),
                        get_file_name(url))
    with open(path_to_file, 'w+'):
        pass
    print(path_to_file)

    return str(path_to_file)


def remove_schema(url):
    if url.startswith('http'):
        new_url = url[8:]
    elif url.startswith('https'):
        new_url = url[9:]
    else:
        new_url = url
    return new_url


def get_file_name(url):
    new_name = []

    for s in remove_schema(url):
        if not s.isalnum():
            new_name.append('-')
        else:
            new_name.append(s)
    new_name.append('.html')
    return ''.join(new_name)
