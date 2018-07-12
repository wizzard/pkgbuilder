from pkgbuilder.pkgbuild import PkgBuild
from pkgbuilder.command import command_exec
from pkgbuilder.local_dir_tree import local_dir_tree


class PkgBuildAutotools(PkgBuild):
    type = "autotools"

    def run(self):
        # autogen.sh
        local_dir_tree.cd(self.src_path)
        exec_cmd = ["./autogen.sh"]
        command_exec(exec_cmd, True)

        super().run()

        # configure
        conf = self.src_path + "/configure"
        exec_cmd = [conf, self.prefix]
        exec_cmd.extend(self.flags)
        command_exec(exec_cmd, True)

        # make
        exec_cmd = ["make"]
        command_exec(exec_cmd, True)

        # make install
        exec_cmd = ["make", "install"]
        command_exec(exec_cmd, True)
