from pkgbuilder.pkgbuild import PkgBuild
from pkgbuilder.command import command_exec
from pkgbuilder.local_dir_tree import local_dir_tree


class PkgBuildAutotools(PkgBuild):
    type = "autotools"

    def prepare(self):
        # autogen.sh in src tree
        local_dir_tree.cd(self.src_path)
        exec_cmd = ["./autogen.sh"]
        command_exec(exec_cmd)

        super().prepare()

        # configure
        conf = self.src_path + "/configure"
        exec_cmd = [conf, self.prefix]
        exec_cmd.extend(self.flags)
        command_exec(exec_cmd)

    def build(self):
        super().build()
        exec_cmd = ["make", "clean"]
        command_exec(exec_cmd)
        exec_cmd = ["make"]
        command_exec(exec_cmd)

    def install(self):
        super().install()
        exec_cmd = ["make", "install"]
        command_exec(exec_cmd)
