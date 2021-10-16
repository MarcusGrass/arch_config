import os

from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.os_io.commands import run_cmd


def fix_git_settings(depth: int, data: InstallData):
    print_on_depth(depth, "Configuring git and generating keys.")
    run_cmd(depth, "git config --global user.email %s" % data.user_opts.email).get_or_throw()
    run_cmd(depth, "git config --global user.name %s" % data.user_opts.user_name).get_or_throw()
    run_cmd(depth, "git config --global pull.rebase true").get_or_throw()
    run_cmd(depth, "git config --global push.default current").get_or_throw()
    run_cmd(depth, "git config --global rerere.enabled true").get_or_throw()

    rsa = data.system_data.append_to_base("/.ssh/id_rsa")
    if not os.path.exists(rsa):
        print_on_depth(depth, "Creating SSH key")
        run_cmd(depth, "ssh-keygen -t rsa -b 4096 -C %s" % data.user_opts.email).get_or_throw()
        run_cmd(depth, "ssh-add %s" % rsa).get_or_throw()
        print_on_depth(depth, "Add the key from ~/.ssh/id_rsa to github to finish git install")
    else:
        print_on_depth(depth, "Skipping key generation as it already exists.")
    print_on_depth(depth, "Success.")


if __name__ == "__main__":
    fix_git_settings(1, InstallData.default())
