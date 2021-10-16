import os
import shutil
import tempfile

from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.opts.user_opts import UserOpts
from pythonmiscscripts.os_io.commands import run_cmd


def install_yay(depth: int):
    print_on_depth(depth, "Installing Yay")
    tmp = tempfile.mkdtemp()
    cur = os.getcwd()
    os.chdir(tmp)
    run_cmd(depth, "git clone https://aur.archlinux.org/yay.git").get_or_throw()
    print_on_depth(depth, "Successfully cloned")
    os.chdir(os.path.join(tmp, "yay"))
    run_cmd(depth, "makepkg -si --noconfirm").get_or_throw()
    print_on_depth(depth, "Successfully installed")
    print_on_depth(depth, "Cleaning up dirs")
    shutil.rmtree(tmp)
    os.chdir(cur)
    print_on_depth(depth, "Success")


if __name__ == "__main__":
    opts = UserOpts.default_opts()
    install_yay(1)
