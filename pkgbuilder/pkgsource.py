class PkgSource(object):
    # remote path of source
    url = None
    # name of package
    name = None
    # type of source
    type = None
    # local path to extracted source
    path = None

    def __init__(self, name, url):
        self.url = url
        self.name = name

    def __str__(self):
        """
        Print the name of the package source
        """
        return self.type

    def get(self):
        """
        Get the sources
        """
        pass

    def update(self):
        """
        Update the sources
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
