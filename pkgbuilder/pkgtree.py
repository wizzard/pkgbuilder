from __future__ import print_function
import logging
import os
import sys
from pkgbuilder.pkg import Pkg
from pkgbuilder.pkg import pkg_get_name
from pkgbuilder.pkgdb import db


class PkgTree(object):
    """
    Perform tasks on the list of packages
    """
    pkgs_dir = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pkgdict = {}

    def set_pkgs_dir(self, pkgs_dir):
        self.pkgs_dir = pkgs_dir

    def get(self, pkg_name):
        """
        Return pkg by name or None
        """
        if pkg_name not in self.pkgdict:
            return None
        return self.pkgdict[pkg_name]

    def load(self):
        """
        Load all pkg files in the directory
        """
        self.logger.debug("Loading packages: %s", self.pkgs_dir)
        for dirpath, _, files in os.walk(self.pkgs_dir):
            for filename in files:
                ext = os.path.splitext(filename)[1]
                fname = os.path.join(dirpath, filename)

                if ext == ".pkg":
                    pkg_name = None
                    # get package name
                    try:
                        pkg_name = pkg_get_name(fname)
                    except (IOError, OSError, ValueError, KeyError) as err:
                        self.logger.error("Failed to load %s package file: %s", fname, err.args)
                        sys.exit(1)

                    self.logger.debug("Loading %s", pkg_name)
                    # see if we have loaded that pkg from database
                    if pkg_name in self.pkgdict:
                        pkg = self.pkgdict[pkg_name]
                    else:
                        pkg = Pkg()
                        pkg.name = pkg_name
                        self.pkgdict[pkg_name] = pkg

                    try:
                        pkg.load(fname)
                    except (IOError, OSError, ValueError, KeyError) as err:
                        self.logger.error("Failed to load %s package file: %s", fname, err.args)
                        sys.exit(1)

    def load_from_db(self):
        """
        Load the list of packages from database
        """
        for pkg_db_entry in db.get_pkg_list():
            pkg_name = pkg_db_entry[0]
            pkg = self.get(pkg_name)
            if pkg is None:
                self.logger.debug("DB package not found: " + pkg_name)
                continue

            self.logger.debug("Loading package: " + pkg_name)
            pkg.load_from_db(pkg_db_entry)

    def get_dependencies(self, pkg, l_order):
        """
        generator, return dependencies for pkg
        """
        for d in pkg.list_depends():
            p1 = self.pkgdict[d]
            if p1 not in l_order:
                l_order.append(p1)
                yield p1
                self.get_dependencies(p1, l_order)

    def get_pkg_list(self):
        """
        generator, return list of all pkgs
        """
        l_order = []
        for pkg in self.pkgdict.values():
            for a in self.get_dependencies(pkg, l_order):
                yield a
            if pkg not in l_order:
                l_order.append(pkg)
                yield pkg

    def list_pkg(self, pkg, spaces):
        """
        print helper function
        """
        for d in pkg.list_depends():
            dpkg = self.pkgdict[d]
            print("{}{}".format(''.join(' ' * spaces), dpkg))
            self.list_pkg(dpkg, spaces + 2)

    def list(self):
        """
        Print pkg list
        """
        for pkg in self.pkgdict.values():
            print(pkg)
            self.list_pkg(pkg, 2)
