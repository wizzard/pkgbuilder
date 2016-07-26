import sqlite3
import logging

class PkgDB(object):
    conn = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load(self, path):
        self.conn = sqlite3.connect(path)

    def get_pkg_list(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM pkgs")

            for row in c.fetchall():
                yield row
        except:
            raise

    def update_pkg(self, pkg):
        try:
            c = self.conn.cursor()
            str = "INSERT OR IGNORE INTO pkgs(name) VALUES('{}')".format(pkg.name)
            self.logger.debug("Updating " + pkg.name + " QUERY: " + str)
            c.execute(str)
        except:
            raise
        else:
            self.conn.commit()

    def delete_pkg(self, pkg):
        try:
            c = self.conn.cursor()
            str = "DELETE FROM pkgs WHERE name='{}'".format(pkg.name)
            self.logger.debug("Updating " + pkg.name + " QUERY: " + str)
            c.execute(str)
        except:
            raise
        else:
            self.conn.commit()
