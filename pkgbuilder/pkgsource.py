import os
from pkgbuilder.local_dir_tree import local_dir_tree


class PkgSource(object):
    # remote path of source
    url = None
    # name of package
    name = None
    # type of source
    type = None
    # local path to extracted source
    src_path = None
    # local path to pkg directory
    pkg_path = None

    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.pkg_path = os.path.join(local_dir_tree.work_dir, self.name)
        self.src_path = os.path.join(self.pkg_path, "src")

    def __str__(self):
        """
        Print the name of the package source
        """
        return self.type

    def init(self):
        """
        Get the sources
        """
        local_dir_tree.rmdir(self.pkg_path)
        local_dir_tree.mkdir(self.pkg_path)

    def update(self):
        """
        Update the sources
        """
        pass

    def exist(self):
        """
        return TRUE if sources exist
        """
        pass


from pkgbuilder.pkgsourcegit import PkgSourceGit
from pkgbuilder.pkgsourcearchieve import PkgSourceArchieve


TypeType = type(type)


def getPkgSource(source_type, name, url):
    pkgSourceClasses = [j for (_, j) in globals().items() if isinstance(j, TypeType) and issubclass(j, PkgSource)]
    for pkgSourceClass in pkgSourceClasses:
        pkg_source = pkgSourceClass(name, url)
        if pkg_source.type == source_type:
            return pkg_source
    raise ValueError("Class not found for source type %s" % source_type)
