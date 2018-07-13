import sqlite3
import logging
from pkgbuilder.conf import conf


class PkgDB(object):
    conn = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load(self, path):
        q = "CREATE TABLE IF NOT EXISTS `pkgs` (`name` TEXT NOT NULL UNIQUE, `date_install` TEXT, `date_update` TEXT, `installed_tag` TEXT, `prev_tag` TEXT, PRIMARY KEY(`name`));"
        if conf.pretend:
            return

        self.conn = sqlite3.connect(path)
        try:
            c = self.conn.cursor()
            c.execute(q)
        except:
            raise
        else:
            self.conn.commit()

    def get_pkg_list(self):
        q = "SELECT name,installed_tag,date_install,date_install,prev_tag FROM pkgs"
        self.logger.debug(q)
        if conf.pretend:
            return

        try:
            c = self.conn.cursor()
            c.execute(q)

            for row in c.fetchall():
                yield row
        except:
            raise

    def update_pkg(self, pkg):
        q = "INSERT OR REPLACE INTO pkgs(name, installed_tag, date_install, date_update, prev_tag) VALUES('{}', '{}', '{}', '{}', '{}')".format(pkg.name, pkg.installed_tag, pkg.installation_date, pkg.update_date, pkg.prev_tag)
        self.logger.debug("Updating " + pkg.name + " QUERY: " + q)
        if conf.pretend:
            return

        try:
            c = self.conn.cursor()
            c.execute(q)
        except:
            raise
        else:
            self.conn.commit()

    def delete_pkg(self, pkg):
        q = "DELETE FROM pkgs WHERE name='{}'".format(pkg.name)
        self.logger.debug(q)
        if conf.pretend:
            return

        try:
            c = self.conn.cursor()
            c.execute(q)
        except:
            raise
        else:
            self.conn.commit()


db = PkgDB()
