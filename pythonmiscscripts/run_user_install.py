from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.install_utils.create_dirs import init_dirs_and_config
from pythonmiscscripts.install_utils.fix_git import fix_git_settings
from pythonmiscscripts.install_utils.install_packages import install_all
from pythonmiscscripts.install_utils.system_fixes import prep_system
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.opts.user_opts import UserOpts
from pythonmiscscripts.os_io.system_data import SystemData
from pythonmiscscripts.templates.templates import from_user_persistence


def install():
    depth = 0
    print_on_depth(depth, "Starting installation run")
    data = gather_info(depth + 1)
    install_all(depth + 1, data)
    fix_git_settings(depth + 1, data)
    init_dirs_and_config(depth, data)
    prep_system(depth, data)


def gather_info(depth: int) -> InstallData:
    opts = from_user_persistence("/home/gramar/code/arch_config/opts")
    system = SystemData(opts.user_name)
    return InstallData(opts, system)


if __name__ == "__main__":
    install()
