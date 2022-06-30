from io import BytesIO
import tarfile
import time


def extends_dict(target, source):
    """ Will copy every key and value of source in target if key is not present in target """
    for key, value in source.items():
        if key not in target:
            target[key] = value
        elif type(target[key]) is dict:
            extends_dict(target[key], value)
        elif type(target[key]) is list:
            target[key] += value
    
    return target

def bytes_to_tarfile(path: str, content):
    tar_file = BytesIO(content)
    
    tar_info = tarfile.TarInfo(name=path)
    tar_info.mtime=time.time()
    tar_info.size=len(content)

    return tar_file, tar_info

def string_to_tarfile(path: str, content: str):
    encoded = content.encode('utf-8')
    tar_file = BytesIO(encoded)

    tar_info = tarfile.TarInfo(name=path)
    tar_info.mtime=time.time()
    tar_info.size=len(encoded)

    return tar_file, tar_info