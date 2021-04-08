from git import Repo


class gitUtils():

    @staticmethod
    def create_repo(path):
        """initialise new repo"""
        new_repo = Repo.init(path)

    @staticmethod
    def create_branch(path, branch):
        """create new branch"""
        repo = Repo(path)
        repo.git.branch(branch)
 
    @staticmethod
    def commit(path_repo : str, branch : str,  **file_add, message_commit : str ):
        repo = Repo(path_repo)
        # Change branch
        repo.git.checkout(branch)
        # Provide a list of the files to stage
        repo.index.add(file_add)
        # Provide a commit message
        repo.index.commit(message_commit)

    
    def tag(path_repo):
        past = cloned_repo.create_tag('past', ref=new_branch,
                              message="This is a tag-object pointing to %s" % new_branch.name)
    """TODO attention
    Il faut parser tous les fichiers et trouver les fichiers pl déjà existants et créer un tag
    """