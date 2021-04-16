import shutil

from pathlib import Path

from django.conf import settings


class FilesUtils():


    @staticmethod
    def create_folder(repo_name, relative_path):
        """create a new folder `repo_name` is the path from path of resources
        and`relative_path`is the path from the repo_name """
        path_repo = os.path.join(settings.MEDIA_ROOT, repo_name)
        path = os.path.join(path_repo, relative_path)
        Path(path).mkdir(parents=True, exist_ok=True)


    @staticmethod
    def delete_folder(repo_name, relative_path):
        """create a new folder `repo_name` is the path from path of resources
        and`relative_path`is the path from the repo_name """
        path_repo = os.path.join(settings.MEDIA_ROOT, repo_name)
        path = os.path.join(path_repo, relative_path)
        shutil.rmtree(path, ignore_errors=True)
