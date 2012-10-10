from datetime import datetime
from functools import wraps
import errno
import os

from unistorage.exceptions import FileNotFound, SuspiciousFilename
from unistorage.interface import Adapter


def assert_exists(fn):
    @wraps(fn)
    def wrapper(self, name):
        try:
            return fn(self, name)
        except (IOError, OSError) as exc:
            if exc.errno == errno.ENOENT:
                raise FileNotFound(name)
            else:
                raise
    return wrapper


class Local(Adapter):
    """
    An adapter for the local filesystem.

    :param directory: the directory where the file storage is located in.
    """
    def __init__(self, directory):
        self.directory = self.normalize_path(directory)

    @assert_exists
    def delete(self, name):
        os.remove(self.compute_path(name))

    def exists(self, name):
        return os.path.exists(self.compute_path(name))

    def list(self):
        for entry in os.listdir(self.directory):
            yield entry

    @assert_exists
    def modified(self, name):
        timestamp = os.path.getmtime(self.compute_path(name))
        return datetime.fromtimestamp(timestamp)

    @assert_exists
    def read(self, name):
        return open(self.compute_path(name)).read()

    @assert_exists
    def size(self, name):
        return os.path.getsize(self.compute_path(name))

    def write(self, name, content):
        with open(self.compute_path(name), 'w') as fp:
            fp.write(content)

    @staticmethod
    def normalize_path(path):
        return os.path.abspath(path)

    def compute_path(self, name):
        """
        Compute the file path in the filesystem from the given name.

        :param name: the filename for which the to compute the path
        :raises SuspiciousFilename: if the computed path is not within
                                    :attr:`directory`.
        """
        path = self.normalize_path(os.path.join(self.directory, name))
        if not path.startswith(self.directory):
            raise SuspiciousFilename(name)
        return path
