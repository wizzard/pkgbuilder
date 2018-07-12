from pkgbuilder.pkgbuild import PkgBuild
from pkgbuilder.command import command_exec


class PkgBuildMeson(PkgBuild):
    type = "meson"

    def run(self):
        super().run()

        # config
        exec_cmd = ["meson", self.src_path, self.prefix]
        exec_cmd.extend(self.flags)
        command_exec(exec_cmd, True)

        # build
        exec_cmd = ["ninja"]
        command_exec(exec_cmd, True)

        # install
        exec_cmd = ["ninja", "install"]
        command_exec(exec_cmd, True)
