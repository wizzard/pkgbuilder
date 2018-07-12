from pkgbuilder.pkgsource import PkgSource
from pkgbuilder.command import command_exec


class PkgSourceGit(PkgSource):
    type = "git"

    def init(self):
        super().init()
        exec_cmd = ["git", "clone", self.url, self.src_path]
        command_exec(exec_cmd, True)

    def update(self):
        exec_cmd = ["git", "pull"]
        command_exec(exec_cmd, True)
