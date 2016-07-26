from __future__ import print_function
import logging
import json
from pkgbuilder.pkgsource import getPkgSource
from pkgbuilder.local_dir_tree import local_dir_tree
from pkgbuilder.command import command_exec


def pkg_get_name(pkg_file):
    """
    Parse JSON and gets the name of package
    """
    try:
        jfile = open(pkg_file)
    except (IOError, OSError) as err:
        print(err.args)
        raise
    else:
        try:
            data = json.load(jfile)
        except ValueError as err:
            raise
        finally:
            jfile.close()
    return data["name"]


class Pkg(object):
    """
    Package object
    """
    pkg_file = None
    depend = []
    description = None
    name = None
    # Souce object
    source = None
    has_pkg_file = False

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        """
        Print the name of the package
        """
        return self.name

    def load(self, pkg_file):
        """
        Load the package file
        """
        self.pkg_file = pkg_file

        self.logger.debug("Loading %s", pkg_file)

        try:
            jfile = open(pkg_file)
        except (IOError, OSError) as err:
            print(err.args)
            raise
        else:
            try:
                data = json.load(jfile)
                self.set_data(data)
            except ValueError as err:
                raise
            finally:
                jfile.close()

    def set_data(self, data):
        """
        Load and parse JSON package file
        """
        self.name = data["name"]
        self.description = data["description"]
        self.depend = list(data["depend"])
        self.source = getPkgSource(data["source"]["type"], data["name"], data["source"]["path"])

    def print_depends(self):
        for d in self.depend:
            print(d)

    def list_depends(self):
        """
        Yield the list of dependencies
        """
        for d in self.depend:
            yield d

    def init(self):
        """
        Get the fresh copy of sources
        """
        self.source.get()

    def build(self):
        """
        Build the package
        """
        local_dir_tree.cd(self.source.path)
        exec_cmd = ["sh", "autogen.sh"]
        command_exec(exec_cmd, True)
        exec_cmd = ["./configure"]
        command_exec(exec_cmd, False)

    def run(self):
        """
        Get, build, install
        """
        self.init()
        self.build()
