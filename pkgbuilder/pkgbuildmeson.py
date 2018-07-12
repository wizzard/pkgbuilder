from pkgbuilder.pkgbuild import PkgBuild
from pkgbuilder.command import command_exec


class PkgBuildMeson(PkgBuild):
    type = "meson"

    def prepare(self):
        super().prepare()
        # config
        exec_cmd = ["meson", self.src_path, self.prefix]
        exec_cmd.extend(self.flags)
        command_exec(exec_cmd)

    def build(self):
        super().build()

        exec_cmd = ["ninja"]
        command_exec(exec_cmd)

    def install(self):
        super().install()
        exec_cmd = ["ninja", "install"]
        command_exec(exec_cmd)
