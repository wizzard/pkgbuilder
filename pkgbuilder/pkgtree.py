from __future__ import print_function
import logging
import os
from pkgbuilder.pkg import Pkg
from pkgbuilder.pkg import pkg_get_name

class PkgTree(object):
    """
    Perform tasks on the list of packages
    """
    pkgs_dir = None
    l_order = []

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

                    pkg.has_pkg_file = True

    def load_from_db(self, db):
        """
        Load the list of packages from database
        """
        for pkg_db_entry in db.get_pkg_list():
            self.logger.debug("Loading package: " + pkg_db_entry[0])
            pkg = Pkg()
            pkg.name = pkg_db_entry[0]
            self.pkgdict[pkg_db_entry[0]] = pkg

    def update_db(self, db):
        """
        Load the list of packages from database
        """
        for pkg in self.pkgdict.values():
            if pkg.has_pkg_file:
                db.update_pkg(pkg)
            else:
                db.delete_pkg(pkg)

    def update(self):
        """
        Update packages
        """
        for pkg in self.pkgdict.values():
            if pkg.has_pkg_file:
                pkg.run()

    def get_dependencies(self, pkg):
        for d in pkg.list_depends():
            p1 = self.pkgdict[d]
            if p1 not in self.l_order:
                self.l_order.append(p1)
                yield p1
                self.get_dependencies(p1)
        #if pkg not in self.l_order:
        #    self.l_order.append(pkg)
        #    yield pkg

    def list_pkg(self, pkg, spaces):
        if pkg.has_pkg_file:
            for d in pkg.list_depends():
                print("{}{}".format(''.join(' ' * spaces), d))
                spaces = spaces + 2
                self.list_pkg(self.pkgdict[d], spaces)

    def list1(self):
        """
        Print pkg list
        """
        for pkg in self.pkgdict.values():
            print("{}".format(pkg.name))
            self.list_pkg(pkg, 2)

    def list(self):
        """
        Print pkg list
        """
        for pkg in self.pkgdict.values():
            for a in self.get_dependencies(pkg):
                print(a.name)
