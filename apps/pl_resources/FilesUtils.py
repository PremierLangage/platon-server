import shutil'
from pathlib import Path


class FilesUtils():


    @staticmethod
    def create_folder(path):
        """create a new folder"""
        Path(path).mkdir(parents=True, exist_ok=True)


    @staticmethod
    def delete_folder(path):
        "delete the folder 'path' and what is in it reccusively"s
        shutil.rmtree(path, ignore_errors=True)

