from __future__ import print_function
import sys
import logging
import argparse
from pkgbuilder.pkglist import PkgList
from pkgbuilder.conf import conf
from pkgbuilder.pkgdb import PkgDB
from pkgbuilder.local_dir_tree import local_dir_tree

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Package manager', usage='''pkgbuilder <action> [<args>]
Actions:
    list     List available packages
    install  Install a packages
    ''')
    parser.add_argument("-c", "--conf", help="Path to the configuration file")
    parser.add_argument("-p", "--path", help="Path to the packages directory", required=True)
    parser.add_argument("-d", "--debug", help="Enable debug output", action="store_true")
    parser.add_argument("--pretend", help="Don't execute any commands", action="store_true")

    #args = parser.parse_args(sys.argv[1:2])
    parser_args = parser.parse_args()

    if not hasattr(self, parser_args.command):
        print('Unrecognized command')
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
    else:
        lvl = logging.INFO
        conf["debug"] = False

    conf["pretend"] = parser_args.pretend

    # Setup logging
    logger = logging.getLogger(__name__)
    #logging.basicConfig(level=lvl, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    logging.basicConfig(level=lvl, format='[%(levelname)s] [%(name)s] %(message)s')

    logger.info("Starting")

    # Open Database
    db = PkgDB()
    try:
        db.load(conf["db_path"])
    except Exception as e:
        print("Failed to open database: {}!".format(conf["db_path"]))
        sys.exit(1)

    pkg_list = PkgList(parser_args.path)

    # load packages from database
    pkg_list.load_from_db(db)

    # prepare local directories
    local_dir_tree.prepare()

    # load packages from file
    try:
        pkg_list.load()
    except Exception as e:
        logger.error("Failed to load packages %s", e.args)

    # clean obsolete directories
    pkg_list.update_db(db)

    try:
        pkg_list.update()
        pkg_list.list()
    finally:
        # Clean up
        local_dir_tree.cd_cwd()

