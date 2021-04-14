import os

from git import Repo

from django.conf import settings


class GitUtils():

    @staticmethod
    def create_repo(repo_name):
        """ Initialize new repo with name `repo_name` and
        with location settings.MEDIA_ROOT.
        Add README file for initialize repository for gitPython
        """
        path_repo = os.path.join(settings.MEDIA_ROOT, repo_name)
        
        # Create repositorie
        repo = Repo.init(path_repo)

        # Initilize repositorie
        filename = os.path.join(path_repo, "README")
        open(filename, 'wb').close()
        repo.index.add(['.'])
        repo.index.commit("Initialize repo")


    @staticmethod
    def create_branch(repo_name, branch_name):
        """create new branch with name `branch_name` on repo `repo_name`
        with location settings.MEDIA_ROOT"""
        repo = Repo(os.path.join(settings.MEDIA_ROOT, repo_name))
        new_branch = repo.create_head(branch_name)
        repo.head.reference = new_branch

 
    @staticmethod
    def commit(repo_name: str, message_commit: str, files_add=['.']):
        """add and commit file `files_add` on repo `repo_name`
        with location settings.MEDIA_ROOT"""
        repo = Repo(os.path.join(settings.MEDIA_ROOT, repo_name))
        repo.index.add(files_add)
        repo.index.commit(message_commit)

    
    def tag(path_repo):
        """ TODO attention
        Il faut parser tous les fichiers et trouver les fichiers
        pl déjà existants et créer un tag"""
        
