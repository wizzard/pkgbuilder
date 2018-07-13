from __future__ import print_function
import logging
import json
from datetime import datetime
from pkgbuilder.pkgsource import getPkgSource
from pkgbuilder.pkgbuild import getPkgBuild
from pkgbuilder.pkgdb import db
from pkgbuilder.conf import conf


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
    depends = []
    description = ""
    name = ""
    installed_tag = ""
    current_tag = ""
    prev_tag = ""
    installation_date = None
    update_date = None

    # Souce object
    source = None
    # Build object
    build = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        """
        Print the name of the package
        """
        return "%s (installed_tag: %s, current_tag: %s)" % (self.name, self.installed_tag, self.current_tag)

    def load(self, pkg_file):
        """
        Load the package file
        """
        self.pkg_file = pkg_file

        self.logger.debug("Loading %s", pkg_file)

        try:
            jfile = open(pkg_file)
        except (IOError, OSError) as err:
            print("%s %s" % ("1", err.args))
            raise
        else:
            try:
                data = json.load(jfile)
                self.set_data(data)
            except ValueError as err:
                print("%s %s" % ("2", err.args))
                raise
            finally:
                jfile.close()

        # try to get current_tag
        try:
            self.current_tag = self.source.get_tag()
        except (IOError, OSError) as err:
            pass

    def set_data(self, data):
        """
        Load and parse JSON package file
        """
        self.name = data["name"]
        self.description = data["description"]
        self.depends = list(data["depend"])
        self.source = getPkgSource(data["source"]["type"], data["name"], data["source"]["path"])
        self.build = getPkgBuild(data["build"]["type"], data["name"], data["build"]["flags"])

    def load_from_db(self, pkg_db_entry):
        self.installed_tag = pkg_db_entry[1]
        self.installation_date = pkg_db_entry[2]
        self.prev_tag = pkg_db_entry[4]
        if not self.prev_tag:
            self.prev_tag = self.installed_tag

    def store_to_db(self):
        pass

    def print_depends(self):
        for d in self.depends:
            print(d)

    def list_depends(self):
        """
        Yield the list of dependencies
        """
        for d in self.depends:
            yield d

    def install(self):
        """
        Initial pkg installation
        """

        if self.current_tag:
            self.logger.debug("Source tree is already fetched")
            self.source.update()
        else:
            self.source.init()

        self.current_tag = self.source.get_tag()

        self.build.prepare()
        self.build.build()
        self.build.install()

        self.installed_tag = self.current_tag
        self.prev_tag = self.installed_tag
        self.installation_date = datetime.now()
        self.update_date = self.installation_date
        db.update_pkg(self)

    def update(self):
        """
        Update installed pkg
        """
        self.source.update()
        self.current_tag = self.source.get_tag()

        if not conf.forced_install and self.current_tag == self.installed_tag:
            self.logger.debug("Latest version already installed")
            return

        self.build.build()
        self.build.install()

        self.update_date = datetime.now()
        self.prev_tag = self.installed_tag
        self.installed_tag = self.current_tag
        db.update_pkg(self)

    def changelog(self):
        """
        display changelog
        """
        print("%s %s %s" % (self.name, self.prev_tag, self.installed_tag))
        output = self.source.get_changelog(self.prev_tag, self.installed_tag)
        print(output)
