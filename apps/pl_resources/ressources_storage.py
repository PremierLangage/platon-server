import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile


class RessourceStorage(FileSystemStorage):

    @staticmethod
    def update(file, content):
        """Update file"""
        with file.open("w+") as f:
            f.write(content)


    @staticmethod
    def open_file(file):
        with file.open("r+") as f:
            return f.readlines()
