import os
from pkgbuilder.pkgsource import PkgSource
from pkgbuilder.command import command_exec
from pkgbuilder.local_dir_tree import local_dir_tree

class PkgSourceGit(PkgSource):
    type = "git"

    def __init__(self, name, url):
        super(PkgSourceGit, self).__init__(name, url)
        self.path = os.path.join(local_dir_tree.work_sources_dir, self.name)

    def get(self):
        exec_cmd = ["git", "clone", self.url, self.path]
        command_exec(exec_cmd, True)
