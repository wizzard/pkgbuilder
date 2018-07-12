from pkgbuilder.pkgsource import PkgSource
from pkgbuilder.command import command_exec


class PkgSourceGit(PkgSource):
    type = "git"

    def init(self):
        super().init()
        exec_cmd = ["git", "clone", self.url, self.src_path]
        command_exec(exec_cmd)

    def update(self):
        super().update()
        exec_cmd = ["git", "pull"]
        command_exec(exec_cmd)

    def get_tag(self):
        super().get_tag()
        exec_cmd = ['git', 'rev-parse', 'HEAD']
        return command_exec(exec_cmd, True)

    def get_changelog(self, old, new):
        super().get_changelog(old, new)
        exec_cmd = ['git', 'log', old + '..' + new]
        return command_exec(exec_cmd, True)
