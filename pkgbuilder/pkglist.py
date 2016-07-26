from __future__ import print_function
import logging
import os
from pkgbuilder.pkg import Pkg
from pkgbuilder.pkg import pkg_get_name


class PkgList(object):
    """
    Perform tasks on the list of packages
    """

    def __init__(self, pkgs_dir):
        self.logger = logging.getLogger(__name__)
        self.pkgs_dir = pkgs_dir
        self.pkgdict = {}

    def load(self):
        """
        Load all pkg files in the directory
        """
        self.logger.debug("Loading packages")
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
        for pkg in self.pkgdict.itervalues():
            if pkg.has_pkg_file:
                db.update_pkg(pkg)
            else:
                db.delete_pkg(pkg)

    def update(self):
        """
        Update packages
        """
        for pkg in self.pkgdict.itervalues():
            if pkg.has_pkg_file:
                pkg.run()

    def list(self):
        """
        Print pkg list
        """
        for pkg in self.pkgdict.itervalues():
            if pkg.has_pkg_file:
                print(">{} {} {}".format(pkg, pkg.source, pkg.source.path))
                for d in pkg.list_depends():
                    print("\t{} -> {}".format(d, self.pkgdict[d].description))
