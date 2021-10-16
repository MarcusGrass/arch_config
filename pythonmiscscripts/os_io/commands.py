import subprocess
from os.path import exists

from pythonmiscscripts.format.printer import format_with_depth, print_on_depth


class CmdResult(object):
    def __init__(self, msg: str, success: bool, depth: int):
        self.msg = msg
        self.success = success
        self.depth = depth

    def was_successful(self) -> bool:
        return self.success

    def get_or_throw(self) -> str:
        if self.success:
            return self.msg
        raise Exception(format_with_depth(self.depth, "Command failed with error: %s" % self.msg))

    def or_print_err(self):
        if not self.success:
            print_on_depth(self.depth, "Cmd caught error: %s" % self.msg)


def pacman_install(depth: int, pkg: str) -> CmdResult:
    return run_cmd(depth, "sudo pacman -S %s --noconfirm --needed" % pkg)


def yay_install(depth: int, pkg: str) -> CmdResult:
    return run_cmd(depth, "yay -S %s --noconfirm --needed" % pkg)


def mkdir(depth: int, abs_path: str, mode=700, username=None) -> CmdResult:
    if not exists(abs_path):
        if username is None:
            mode = 644
        run_cmd(depth, "sudo mkdir -p %s -m %s" % (abs_path, mode)).get_or_throw()
        if username is not None:
            run_cmd(depth, "sudo chown %s -R %s" % (username, abs_path)).get_or_throw()
            res = run_cmd(depth, "sudo chgrp %s -R %s" % (username, abs_path))
            res.get_or_throw()
            return res

    return CmdResult(msg="Success", success=True, depth=depth)


def mkfile(depth: int, abs_path: str, username=None) -> bool:
    if not exists(abs_path):
        run_cmd(depth, "sudo touch %s" % abs_path).get_or_throw()

        if username is not None:
            run_cmd(depth, "sudo chown %s %s" % (username, abs_path)).get_or_throw()
            res = run_cmd(depth, "sudo chgrp %s %s" % (username, abs_path))
            res.get_or_throw()
        return True

    return False


def run_cmd(depth: int, cmd, piped_input=None) -> CmdResult:
    proc = subprocess.Popen(cmd.split(" "),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    if piped_input is not None:
        proc.stdin.write(piped_input.encode("utf-8"))
    out, err = proc.communicate()
    if out is None:
        return CmdResult(err.decode("utf-8"), False, depth)

    return CmdResult(out.decode("utf-8"), True, depth)


if __name__ == "__main__":
    # print(mkdir(1, "/home/gramar/test/t", 700, True, "gramar").get_or_throw())
    # print(mkfile(1, "/home/gramar/tst.txt", username="gramar"))
    # sudo_mkdir(1, "/etc/X11/pp", 777)
    pass
