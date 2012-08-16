class Storage(object):
    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, name):
        """
        Return ``True`` if `name` refers to an existing container within
        this storage, or ``False`` if the name is available for a new
        container.
        """
        raise NotImplementedError


class Container(object):

    def __init__(self, storage, name):
        self.storage = storage
        self.name = name

    def __len__(self):
        """
        Return the number of files in this container.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Return a generator over the files in this container.
        """
        raise NotImplementedError

    def __contains__(self, name):
        """
        Return ``True`` if `name` refers to an existing file within this
        container, or ``False`` if the name is available for a new file.

        :param name: the name of the file to check for existence
        """
        raise NotImplementedError

    def __getitem__(self, name):
        """
        Return an :class:`File` instance for an existing file.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :param name: the name of the file to retrieve
        :return: a :class:`File` representing the file requested
        """
        raise NotImplementedError

    def __str__(self):
        return self.name


class File(object):

    def __init__(self, container, name, mode):
        self.container = container
        self.name = name
        self._mode = mode

    @property
    def accessed(self):
        """
        A :class:`datetime.datetime` object representing the last time
        this file was accessed.
        """
        raise NotImplementedError

    @property
    def closed(self):
        """
        A boolean indicating whether the file is closed.
        """
        raise NotImplementedError

    @property
    def created(self):
        """
        A :class:`datetime.datetime` object representing the time this
        file was created.
        """
        raise NotImplementedError

    @property
    def mode(self):
        """
        The read/write mode for the file.
        """
        return self._mode

    @property
    def modified(self):
        """
        A :class:`datetime.datetime` object representing the last time
        this file was modified.
        """
        raise NotImplementedError

    @property
    def size(self):
        """
        The size of this file in bytes.
        """
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    def exists(self):
        pass

    def delete(self):
        """
        Delete this file.
        """

    def read(self, num_bytes=None):
        """
        Read content from the file.

        :param num_bytes: the number of bytes to read; if not specified
            the file will be read to the end.
        """
        raise NotImplementedError

    def write(self, content):
        """
        Write content to the file.

        Depending on the storage system behind the scenes, this content
        might not be fully committed until :method:`close` is called on
        the file.

        :param content: a string or `file`-like object to write to the
            file.
        """
        raise NotImplementedError

    def close(self):
        """
        Close the file.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Iterate over the file yielding one line at a time.
        """
        raise NotImplementedError

    def __len__(self):
        return self.size

    def __str__(self):
        return self.name
