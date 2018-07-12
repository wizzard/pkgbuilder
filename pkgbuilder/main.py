from __future__ import print_function
import sys
import logging
import argparse
from pkgbuilder.pkgtree import PkgTree
from pkgbuilder.conf import conf
from pkgbuilder.pkgdb import PkgDB
from pkgbuilder.local_dir_tree import local_dir_tree

class App(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = PkgDB()
        self.pkg_tree = PkgTree()

    def install(self, params=None):
        if not params:
            self.logger.error("No package to install specified")
            return False

        for p in params:

            if not self.pkg_tree.get(p):
                self.logger.error("Package '%s' specification not found", p)
                return False

            pkg = self.pkg_tree.get(p)
            for dep in self.pkg_tree.get_dependencies(pkg):
                self.logger.info("Installing %s", dep)
                dep.source.init()
                dep.build.run()

            self.logger.info("Installing %s", pkg)
            pkg.source.init()
            pkg.build.run()

        return True

    def list(self, params=None):
        self.logger.info("Listing")
        self.pkg_tree.list()

    def update(self, params=None):
        self.logger.info("Updating")
        try:
            self.pkg_tree.update()
        finally:
            # Clean up
            local_dir_tree.cd_cwd()


    def run(self):
        # Parse arguments
        parser = argparse.ArgumentParser(description='Package manager', usage='''pkgbuilder <action> [<args>]
    Actions:
        list                    List available packages
        install [pkg1,pkg2]     Install package(-s)
        update [pkg1,pkg2]      Update package(-s) or all packages, if no pkg is specified
        ''')
        parser.add_argument("action", help="Command to run")
        parser.add_argument("params", help="action parameter(-s)", nargs='*')
        parser.add_argument("-c", "--conf", help="Path to the configuration file")
        parser.add_argument("-p", "--path", help="Path to the packages directory")
        parser.add_argument("-d", "--debug", help="Enable debug output", action="store_true")
        parser.add_argument("--pretend", help="Don't execute any commands", action="store_true")

        try:
            parser_args = parser.parse_args()
        except:
            parser.print_help()
            exit(1)

        if not hasattr(self, parser_args.action):
            parser.print_help()
            exit(1)

        if not parser_args.conf:
            parser_args.conf = "pkgbuilder.conf"

        try:
            conf.load(parser_args.conf)
        except:
            print("Failed to read configuration file: {}!".format(parser_args.conf))
            sys.exit(1)

        lvl = logging.DEBUG
        if parser_args.debug:
            #lvl = logging.DEBUG
            conf["debug"] = True
            sys.dont_write_bytecode = True
        else:
            lvl = logging.INFO
            conf["debug"] = False

        conf["pretend"] = parser_args.pretend

        # Setup logging
        logging.basicConfig(level=lvl, format='[%(levelname)s] [%(name)s] %(message)s')

        self.logger.info("Starting")

        self.pkg_tree.set_pkgs_dir(parser_args.path)

        # Open Database
        try:
            self.db.load(conf["db_path"])
        except Exception as e:
            print("Failed to open database: {}!".format(conf["db_path"]))
            sys.exit(1)

        # load packages from database
        # self.pkg_tree.load_from_db(self.db)

        # prepare local directories
        local_dir_tree.prepare()

        # load packages from file
        try:
            self.pkg_tree.load()
        except Exception as e:
            self.logger.error("Failed to load packages %s", e.args)

        # clean obsolete directories
        self.pkg_tree.update_db(self.db)

        # execute specified command
        getattr(self, parser_args.action)(parser_args.params)
