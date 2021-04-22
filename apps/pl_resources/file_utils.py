import shutil
import os

from pathlib import Path

from django.conf import settings


class FilesUtils():


    @staticmethod
    def create_folder(path_repo):
        """create a new folder `repo_name` is the path from path of resources
        and`relative_path`is the path from the repo_name """
        
        path = os.path.join(settings.MEDIA_ROOT, path_repo)
        if not os.path.exists(path):
            Path(path).mkdir(parents=True, exist_ok=True)


    @staticmethod
    def delete_folder(path_repo):
        """create a new folder `repo_name` is the path from path of resources
        and`relative_path`is the path from the repo_name """
        path = os.path.join(settings.MEDIA_ROOT, path_repo)
        try:
            os.rmdir(path)
        except Exception:
            return False
        return True

    
    @staticmethod
    def delete_file(path_file):
        """delete file"""
        path = os.path.join(settings.MEDIA_ROOT, path_file)
        shutil.rmtree(path, ignore_errors=True)
