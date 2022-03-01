#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  files.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

# https://azzamsa.com/n/gitpython-intro/
# https://www.devdungeon.com/content/working-git-repositories-python
# https://github.com/ishepard/pydriller/blob/master/pydriller/git.py

from __future__ import annotations


import os
import shutil
import subprocess
import tempfile
import datetime
import uuid


from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, TypedDict, Union
from wsgiref.util import FileWrapper


from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import HttpResponse
from git import Actor, Repo
from git.objects import Blob, Tree
from git.exc import GitCommandError
from rest_framework.request import Request
from rest_framework.reverse import reverse

User = get_user_model()
DIRECTORIES_ROOT = settings.DIRECTORIES_ROOT


def uniquify_filename(directory, filename) -> Tuple[str, str]:
    """Makes sure that "filename" is unique inside "directory".

    If a file already exists with the given name, the function will compute the name
    and add "(n)" before the extension, where n is the first number found such
    that the file does not already exist.

    Args:

        directory (`Union[str, Path]`): Some directory path.
        filename: (`str`): The name of the file to create.

    Returns:
    (abspath, filename) where "abspath" is the absolute path of the file and "filename" is the name of the file
    """

    name, ext = os.path.splitext(filename)
    filename = f"{name}{ext}"
    abspath = os.path.join(str(directory), filename)

    counter = 1
    while os.path.exists(abspath):
        filename = f"{name}({counter}){ext}"
        abspath = os.path.join(directory, filename)
        counter += 1

    return abspath, filename


class Version(TypedDict):
    name: str
    date: datetime.datetime
    message: str
    url: str


class TreeNode(TypedDict):
    path: str
    parent: str
    type: Literal['file', 'folder']
    children: Optional[List['TreeNode']]


class Directory:
    """Representation of a versioned directory.
    """

    def __init__(self, root: Path, user: User):
        self.root = root.resolve()
        self.user = user
        self.ignore_commits = False
        self.repo = Repo(root)

        if user:
            with self.repo.config_writer() as cw:
                cw.set_value('user', 'name', user.username)
                cw.set_value('user', 'email', getattr(user, 'email', 'admin@platon'))
                cw.release()
        else:
            with self.repo.config_writer() as cw:
                cw.set_value('user', 'name', 'admin')
                cw.set_value('user', 'email', getattr(user, 'email', 'admin@platon'))
                cw.release()


    # STATIC


    @classmethod
    def get(cls, name: str, user: User = None) -> 'Directory':
        """Finds the directory named `name`.

        Args:
            name (`str`): Name of the directory to find.
                A directory name is a string in the following format
                `type:id` where `type` is one of '[r, c]' for resource and circle
                and `id` is the identifier of a circle or resource.

        Raises:
            `FileNotFoundError`: If the directory does not exists.

        Returns:
            `Directory`: A Directory object.
        """

        path = Path(os.path.join(DIRECTORIES_ROOT, str(name)))
        if not path.exists():
            raise FileNotFoundError(f'{name}: No such file or directory')
        return cls(path, user)

    @classmethod
    def create(cls, name: str, user: User = None) -> 'Directory':
        """Creates new directory tree.

        Args:
            name (`str`): Name of the directory to create.
        Returns:
            `Directory`: A Directory object.
        """

        path = Path(os.path.join(DIRECTORIES_ROOT, str(name)))
        if path.exists():
            return cls.get(name, user)

        path.mkdir(parents=True, exist_ok=True)
        Repo.init(path)

        directory = cls(path, user)

        # create a file to force git to create master branch
        directory.create_file('.keep')
        directory.commit('init')

        return directory

    @classmethod
    def delete(cls, name: str):
        """Recursively delete a directory.

        Args:
            name (`str`): Name of the directory to delete.
        Returns:
            `bool`: `True` if deleted `False` otherwise.
        """

        path = Path(os.path.join(DIRECTORIES_ROOT, str(name)))
        if not path.exists():
            return False
        shutil.rmtree(path)
        return True


    def exists(self, path: str):
        """Checks whether the given `path` exists inside the directory.

        Args:
            path (`str`): A path relative to the directory.

        Raises:
            `TypeError`: If `path` is null or empty.
            `PermissionError`: If `path` points to a file outside of the directory.

        Returns:
            `str`: `True` if the path exists.
        """

        return self.__as_abspath(path).exists()

    def is_dir(self, path: str):
        """Checks whether the given `path` points to a directory.

        Args:
            path (`str`): A path relative to the directory.

        Raises:
            `TypeError`: If `path` is null or empty.
            `PermissionError`: If `path` points to a file outside of the current directory.

        Returns:
            `str`: `True` if the path points to a directory.
        """

        return self.__as_abspath(path).is_dir()

    def is_file(self, path: str):
        """Checks whether the given `path` points to a regular file.

        Args:
            path (`str`): A path relative to the directory.

        Raises:
            `TypeError`: If `path` is null or empty.
            `PermissionError`: If `path` points to a file outside of the current directory.

        Returns:
            `str`: `True` if the path points to a regular file.
        """

        return self.__as_abspath(path).is_file()


    def move(self, src: str, dst: str, copy: bool = False):
        """Moves the file/folder `src` to `dst`

        Args:
            src (`str`): Source file/directory path to move relative to the current directory.
            dst (`str`): Target directory path relative to the current directory.
            copy (`bool`): Copy Source instead of moving it if defined to `True`.

        Raises:
            `TypeError`: If any of `src` or `dst` is null or empty.
            `PermissionError`: If the operation is not permitted.
        """

        abs_src_path = self.__as_abspath(src)
        abs_dst_path = self.__as_abspath(dst, authorize_root=True)

        if not abs_dst_path.is_dir():
            raise NotADirectoryError(f"[Errno 20] No such directory: '{dst}'")

        # move inside the same directory
        if not copy and abs_src_path.parent.samefile(abs_dst_path):
            return

        abs_dst_path, _ = uniquify_filename(abs_dst_path, abs_src_path.name)

        if copy:
            if os.path.isdir(abs_src_path):
                shutil.copytree(abs_src_path, abs_dst_path)
            else:
                shutil.copyfile(abs_src_path, abs_dst_path)
        else:
            shutil.move(abs_src_path, abs_dst_path)

        self.commit(f'move {src} to {dst}')

    def remove(self, path: str):
        """Delete the file/folder at the given `path`.

        Args:
            path (`str`): A path relative to the directory.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If `path` does not exists.
            `PermissionError`: If `oldpath` or `newpath` points to a file outside of the current directory.
        """

        abspath = self.__as_abspath(path)
        if not abspath.exists():
            raise FileNotFoundError(f'{path}: does not points to a valid file')

        if abspath.is_file():
            abspath.unlink()
        elif abspath.is_dir():
            shutil.rmtree(abspath)

        self.commit(f'delete {path}')

        return True

    def rename(self, oldpath: str, newpath: str):
        """Rename `oldpath` to `newpath`.

        Args:
            oldpath (str): Path to the file to rename (relative to the current directory).
            newpath (str): Path to the new file name (relative to the current directory).

        Raises:
            `FileNotFoundError`: If `oldpath` does not points to an existing file.
            `FileExistsError`: If `newpath` points to an existing file.
            `PermissionError`: If `oldpath` or `newpath` points to a file outside of the current directory.
            `PermissionError`: If `oldpath` and `newpath` does not have the same parent.
        """

        oabspath = self.__as_abspath(oldpath)
        nabspath = self.__as_abspath(newpath)

        if not oabspath.exists():
            raise FileNotFoundError(
                f'"{oldpath}"" does not points to a valid file')

        if nabspath.exists():
            raise FileExistsError(f'"{newpath}"" points to an existing file')

        if not oabspath.parent.samefile(nabspath.parent):
            raise PermissionError(
                'new file name should be inside the same directory')

        oabspath.rename(nabspath)

        self.commit(f'rename {oldpath} to {newpath}')

    def create_dir(self, path: str):
        """Creates a new directory at the given `path`

        Args:
            path (`str`): A path relative to the directory.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If parent of  `path` does not points to an existing directory.
            `FileExistsError`: If `path` points to an existing file.
            `PermissionError`: If `path` points to a file outside of the current directory.
        """

        abspath = self.__as_abspath(path)
        abspath.mkdir(parents=False, exist_ok=False)
        abspath.joinpath('./.keep').touch()  # allow to list empty directories
        self.commit(f'create {path}')

    def create_file(self, path: str, content: str = None):
        """Creates a new file at the given `path`

        Args:
            path (`str`): A path relative to the current directory.
            path (`str`, optional): Initial content of the file.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If parent of `path` does not points to an existing directory.
            `FileExistsError`: If `path` points to an existing file.
            `PermissionError`: If `path` points to a file outside of the current directory.
        """

        abspath = self.__as_abspath(path)
        abspath.touch(exist_ok=False)
        if content:
            abspath.write_text(content)

        self.commit(f'create {path}')

    # WRITE

    def write_text(self, path: str, data: str):
        """Write text at the given `path`

        Args:
            path (`str`): A path relative to the directory.
            data (str): Text to write.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If `path` does not points to an existing file.
            `FileExistsError`: If `path` points to an existing file.
            `PermissionError`: If `path` points to a file outside of the current directory.
        """

        abspath = self.__as_abspath(path)
        abspath.write_text(data)

        self.commit(f'update {path}')

    def write_bytes(self, path: str, data: bytes):
        """Write bytes at the given `path`

        Args:
            path (`str`): A path relative to the directory.
            data (str): Bytes to write.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If `path` does not points to an existing file.
            `FileExistsError`: If `path` points to an existing file.
            `PermissionError`: If `path` points to a file outside of the current directory.
        """

        abspath = self.__as_abspath(path)
        abspath.write_bytes(data)

        self.commit(f'update {path}')

    def write_file(
        self,
        path: str,
        data: InMemoryUploadedFile,
        unzip: bool = True
    ):
        """Upload file at the given `path`

        Args:
            path (`str`): A path relative to the directory.
            data: File to write.

        Raises:
            `TypeError`: If `path` is null or empty.
            `FileNotFoundError`: If `path` does not points to an existing file.
            `FileExistsError`: If `path` points to an existing file.
            `PermissionError`: If `path` points to a file outside of the current directory.
        """

        path = "." if not path else path
        abspath = self.__as_abspath(path, authorize_root=True)

        if not abspath.is_dir():
            raise NotADirectoryError("[Errno 20] No such directory: '{path}'")

        abspath, _ = uniquify_filename(abspath, data.name)
        abspath = Path(abspath)

        with abspath.open('wb+') as destfile:
            for chunk in data.chunks():
                destfile.write(chunk)

        if unzip and data.content_type == 'application/zip':
            shutil.unpack_archive(abspath, abspath.parent)
            abspath.unlink()  # delete the zip

        self.commit(f'upload {data.name} into {path}')

    # READ

    def read(
        self,
        path: str = ".",
        version: str = "master",
        request: Request = None
    ) -> Union[bytes, List[TreeNode]]:
        """Gets the file tree or the file at the given `path` for the given the `version`.

        Args:
            path (`str`, optional): Path to a file/directory. Defaults to `.` which means the root.
            version (`str`, optional): Specify which version (v1..vN) to find. Defaults to "master".

        Returns:
            List[TreeNode]: A recursive list of TreeNode objects.
            Bytes: Content of the file.
        """

        path = "." if not path else path
        object = self.repo.tree(version)

        if path != ".":
            object = object[path]

        if object.type == "tree":
            return self.__list_files(object, path, version, request=request)

        return object.data_stream.read()

    def search(
        self,
        query: str,
        path: str = ".",
        version: str = "master",
        match_word: bool = False,
        match_case: bool = False,
        use_regex: bool = False
    ):
        if not query:
            raise TypeError('argument "query" is missing')

        args = []
        args.append("-I")  # no binary files
        if not use_regex:
            args.append("-F")

        args.append("--full-name")  # forces paths to be output relative to repo root
        args.append("-n")  # line numbers

        if match_word:
            args.append("-w")

        if not match_case:
            args.append('-i')

        args.append(f'"{query}"')
        args.append(version)

        if path != "." and path != '':
            args.append("--")
            args.append(path)

        # https://git-scm.com/docs/git-grep
        cwd = os.getcwd()
        try:
            os.chdir(self.root)
            command = "git grep " + " ".join(args)
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            out, err = p.communicate()
        finally:
            os.chdir(cwd)
        ret, out, err = p.returncode, out.decode().strip("\n"), err.decode()

        prefix = len(f'{version}:')

        def parse_match(match):
            match = match[prefix:]
            tokens = match.split(':')
            return {
                "path": tokens[0],
                "line": tokens[1],
                "match": "".join(tokens[2:])
            }

        if not err:
            return [] if not out else ([parse_match(m) for m in out.split('\n')])
        else:  # pragma: no cover
            raise Exception(f'{out}: {err}')

    # GIT
    
    def checkout(self, tag_name):
        self.repo.git().checkout(tag_name)
        

    def merge(self, bundle: InMemoryUploadedFile) -> Any:
        path = os.path.join(DIRECTORIES_ROOT, str(uuid.uuid4()) + '.git')
        with open(path, 'wb+') as file:
            for chunk in bundle.chunks():
                file.write(chunk)
        self.repo.git.pull(path)
        Path(path).unlink()

    def commit(self, message: str) -> bool:
        if self.ignore_commits:
            return False

        if not self.repo.is_dirty(untracked_files=True):
            return False

        self.repo.git.add('--all')
        author = None
        committer = None
        if self.user:
            author = Actor(self.user.username, self.user.email)
            committer = Actor(self.user.username, self.user.email)

        self.repo.index.commit(message, author=author, committer=committer)

        return True

    def describe(self) -> str:
        return self.repo.git.describe('--always')

    def bundle(self, version: str = "master") -> HttpResponse:
        path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.git')
        self.repo.git.bundle('create', path, 'HEAD', version)
        with open(path, 'rb') as file:
            response = HttpResponse(content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename=bundle.git'
            response.write(file.read())
            return response

    def download(self, path: str = '.', version: str = "master") -> HttpResponse:
        abspath = self.__as_abspath(path, authorize_root=True)
        if abspath.is_file():
            tree = self.repo.tree(version)
            response = HttpResponse(content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'
            response.write(tree[path].data_stream.read())
            return response

        relpath = str(abspath.relative_to(self.root))
        with NamedTemporaryFile(suffix='.zip') as zip:
            self.repo.archive(zip, version, path=None if relpath == "." else relpath)

            # https://docs.python.org/3/library/tempfile.html#examples
            zip.seek(0)

            response = HttpResponse(FileWrapper(zip), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename=archive.zip'
            return response

    def list_versions(self, request=None) -> List[Version]:
        """List all versions of the directory.
        """
        url = reverse('pl_resources:files', request = request, kwargs = {'directory': self.root.name})
        return [
            {
                'name': item.name,
                'date': datetime.datetime.fromtimestamp(item.tag.tagged_date),
                'message': item.tag.message,
                'url': f'{url}?version={item.name}' 
            }
            for item in self.repo.tags
        ]

    def create_version(self, message: str, request= None) -> Version:
        """Creates new version of the directory by tagging the current git index.

        Args:
            name (`str`): Name of the release.
            message (`str`): Message associated to the release.

        Returns:
            `Version`: The newly created version.
        """

        url = reverse('pl_resources:files', request = request, kwargs = {'directory': self.root.name})
        n_versions = len(self.list_versions()) + 1
        object = self.repo.create_tag(str(n_versions), message=message)

        return {
            'name': object.name,
            'date': datetime.datetime.fromtimestamp(object.tag.tagged_date),
            'message': object.tag.message,
            'url': f'{url}?version={object.name}'
        }
        
    def release(self, message: str, request=None):
        self.commit(message)
        self.create_version(message, request)
        
    # PRIVATE


    def __iterate(self, object: Union[Tree, Blob], version: str, request=None) -> TreeNode:
        node: TreeNode = {
            'path': object.path,
            'size': object.size,
            'type': 'folder' if object.type == 'tree' else 'file',
            'hexsha': object.hexsha
        }

        if node['type'] == 'folder':
            children: List[TreeNode] = []
            for o in object:
                if os.path.basename(o.path).startswith('.'):
                    continue
                children.append(self.__iterate(o, version, request))

            node['children'] = sorted(
                children,
                key=lambda x: (x['type'], x['path'])
            )
        else:
            node['mime'] = object.mime_type

        if request:
            self.__build_urls(node, version, request)

        return node

    def __build_urls(self, object: Any, version: str, request):
        kwargs = {
            'directory': self.root.name,
        }

        if object['path'] != '.':
            kwargs['path'] = object['path']
        url = reverse('pl_resources:files', request=request, kwargs=kwargs)
        object['url'] = f'{url}?version={version}'
        object['download_url'] = f'{url}?version={version}&download'
        if object['path'] == '.':
            object['bundle_url'] = f'{url}?version={version}&git-bundle'
            object['describe_url'] = f'{url}?version={version}&git-describe'

    def __list_files(self,
                     tree: Tree,
                     path: str,
                     version: str,
                     request=None):
        relpath = str(self.root.joinpath(path).relative_to(self.root))

        response = {
            'path': relpath,
            'hexsha': tree.hexsha,
            'version': version,
            'versions': self.list_versions(request),
            'directory': self.root.name,
        }

        if request:
            self.__build_urls(response, version, request)

        response['files'] = self.__iterate(tree, version, request)['children']
        return response

    def __as_abspath(self, path: str = '.', authorize_root: bool = False) -> Path:
        if path is None:
            raise TypeError('argument "path" is required')

        path = path.strip()
        if path.startswith('/'):
            raise PermissionError(f'{path}: should not starts with "/"')

        if path == '.':
            if authorize_root:
                return self.root
            raise TypeError('argument "path" is required')

        abspath = Path(os.path.join(self.root, path)).resolve()

        # ensure that path does not point to a file outside of self.root
        if not abspath.is_relative_to(self.root):
            raise PermissionError(f'{path}: points to an invalid file')

        return abspath
