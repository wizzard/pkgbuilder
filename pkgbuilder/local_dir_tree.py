import os
import errno
import logging
from pkgbuilder.conf import conf

class LocalDirTree(object):
    """
    Perform local directory tasks
    """
    work_sources_dir = None

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
        self.work_sources_dir = os.path.join(conf["work_dir_path"], conf["work_sources_dir"])
        self.mkdir(self.work_sources_dir)

local_dir_tree = LocalDirTree()
