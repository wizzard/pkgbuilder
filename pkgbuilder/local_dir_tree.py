import os
import errno
import logging
from shutil import rmtree
from pkgbuilder.conf import conf


class LocalDirTree(object):
    """
    Perform local directory tasks
    """
    work_dir = None
    root_dir = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cwd = os.getcwd()

    def mkdir(self, path):
        """
        Create directory (with parents), ignore exception if it exists
        """
        self.logger.debug("Creating dir: %s", path)
        if conf.pretend:
            return

        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def rmdir(self, dir_path):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("rmtree %s", dir_path)
        if conf.pretend:
            return
        rmtree(dir_path, True)


    def cd(self, path):
        self.logger.debug("Changing dir: %s", path)
        if conf.pretend:
            return

        try:
            os.chdir(path)
        except:
            raise

    def cd_cwd(self):
        self.cd(self.cwd)

    def prepare(self):
        self.work_dir = conf["work_dir"]
        self.mkdir(self.work_dir)
        self.root_dir = conf["root_dir"]
        self.mkdir(self.root_dir)


local_dir_tree = LocalDirTree()
