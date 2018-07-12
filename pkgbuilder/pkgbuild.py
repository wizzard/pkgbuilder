import os
from pkgbuilder.local_dir_tree import local_dir_tree


class PkgBuild(object):
    # name of package
    name = None
    # type of build
    type = None
    # local path to build directory
    build_path = None
    # local path to src directory
    src_path = None
    # local path to pkg directory
    pkg_path = None
    prefix = ""
    flags = []

    def __init__(self, name, flags):
        self.name = name
        self.pkg_path = os.path.join(local_dir_tree.work_dir, self.name)
        self.build_path = os.path.join(self.pkg_path, "build")
        self.src_path = os.path.join(self.pkg_path, "src")
        self.prefix = "--prefix=" + local_dir_tree.root_dir
        self.flags = flags

    def __str__(self):
        """
        Print the name of the package build
        """
        return self.type

    def run(self):
        """
        Build the sources
        """
        local_dir_tree.rmdir(self.build_path)
        local_dir_tree.mkdir(self.build_path)
        local_dir_tree.cd(self.build_path)

    def exist(self):
        """
        return TRUE if sources exist
        """
        pass


from pkgbuilder.pkgbuildautotools import PkgBuildAutotools
from pkgbuilder.pkgbuildmeson import PkgBuildMeson


TypeType = type(type)


def getPkgBuild(build_type, name, flags):
    pkgBuildClasses = [j for (_, j) in globals().items() if isinstance(j, TypeType) and issubclass(j, PkgBuild)]
    for pkgBuildClass in pkgBuildClasses:
        pkg_build = pkgBuildClass(name, flags)
        if pkg_build.type == build_type:
            return pkg_build
    raise ValueError("Class not found for build type %s" % build_type)
