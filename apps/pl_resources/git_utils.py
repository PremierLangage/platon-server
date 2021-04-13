import os

from git import Repo

from django.conf import settings


class GitUtils():

    @staticmethod
    def create_repo(name):
        """initialise new repo"""

        # Create repositorie
        repo = Repo.init(os.path.join(settings.MEDIA_ROOT, name))

        # Initilize repositorie
        filename = os.path.join(settings.MEDIA_ROOT, "README")
        open(filename, 'wb').close()
        repo.index.add(['.'])
        repo.index.commit("Initialize repo")

    @staticmethod
    def create_branch(name, branch):
        """create new branch"""
        repo = Repo(os.path.join(settings.MEDIA_ROOT, name))
        new_branch = repo.create_head(branch)
        repo.head.reference = new_branch

 
    @staticmethod
    def commit(name: str, branch: str,  file_add, message_commit: str):
        repo = Repo(os.path.join(settings.MEDIA_ROOT, name))
        repo.index.add(['.'])
        repo.index.commit("Initialize repo")

    
    def tag(path_repo):
        """ TODO attention
        Il faut parser tous les fichiers et trouver les fichiers
        pl déjà existants et créer un tag"""
        
