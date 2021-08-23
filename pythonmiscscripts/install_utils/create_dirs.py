import os
import shutil

from pythonmiscscripts.chroot.prep_env import create_with_content
from pythonmiscscripts.file_manipulation.eof_append import append_lines_to_end
from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.input_utils.parse_input import confirm
from pythonmiscscripts.opts.install_data import InstallData
from pythonmiscscripts.os_io.commands import mkdir, mkfile
from pythonmiscscripts.templates.templates import to_xmobarrc

BASE = [
    "/pictures/screenshots",
    "/pictures/wps",
    "/code/java",
    "/code/python",
    "/code/bash",
    "/code/rust",
    "/code/unclassified",
    "/documents",
    "/downloads/",
    "/misc",
    "/misc/screensavers",
]

USER_COPY_DIRS = [
    "/.xmonad",
    "/.gnupg",
    "/.ssh",
    "/.config",
]

SYS_DIRS = [
    "/etc"
]


def init_dirs_and_config(depth: int, data: InstallData):
    print_on_depth(depth, "Initialising dirs")
    create_dirs(depth, data)
    copy_user_files(depth, data)
    copy_dirs(depth, data)


def create_dirs(depth: int, data: InstallData):
    for d in BASE:
        os.makedirs(data.system_data.append_to_base(d), mode=0o700, exist_ok=True)
        print_on_depth(depth, "Created dir: %s" % d)


def copy_dirs(depth: int, data: InstallData):
    for d in USER_COPY_DIRS:
        dest = data.system_data.append_to_base("/")
        cfg = data.system_data.append_to_config_location(d)
        if not os.path.exists(dest):
            mkdir(depth, dest, username=data.user_opts.user_name)
        copy_corresponding(depth, dest, cfg, data)
        print_on_depth(depth, "Copied contents of dir %s" % d)
    for d in SYS_DIRS:
        dest = d
        cfg = data.system_data.append_to_config_location(d)
        if not os.path.exists(dest):
            mkdir(depth, dest)
        copy_corresponding(depth, dest, cfg, data)  # TODO: Fix bug where it tries to copy to /etcetc
        print_on_depth(depth, "Copied contents of dir %s" % d)


def copy_corresponding(depth: int, dest_root, cfg, data: InstallData):
    for root, dirs, files in os.walk(cfg):
        cor = str(root).replace(data.system_data.append_to_config_location("/"), "")
        dest = dest_root + cor
        if not os.path.exists(dest):
            os.makedirs(dest, mode=0o700, exist_ok=True)
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(dest, f)
            abs_copy(depth, src, dst)
            print_on_depth(depth, "Copied %s")


def copy_user_files(depth: int, data: InstallData):
    copy(depth, "/.xinitrc", data.system_data.append_to_base("/.xinitrc"), data)
    copy(depth, "/.Xresources", data.system_data.append_to_base("/.Xresources"), data)
    copy(depth, "/.xscreensaver", data.system_data.append_to_base("/.xscreensaver"), data)
    copy(depth, "/.bashrc", data.system_data.append_to_base("/.bashrc"), data)
    copy(depth, "/.ideavimrc", data.system_data.append_to_base("/.ideavimrc"), data)
    copy(depth, "/.vimrc", data.system_data.append_to_base("/.vimrc"), data)


def copy(depth: int, config_relative: str, abs_dest: str, data: InstallData):
    path = data.system_data.append_to_config_location(config_relative)
    abs_copy(depth, path, abs_dest)


def abs_copy(depth: int, src: str, dest: str):
    if os.path.exists(dest):
        if confirm(depth, "A file exists at %s continue and backup?\n" % dest):
            shutil.copy(dest, dest + ".bak.cfg")
            shutil.copy(src, dest)
        else:
            print_on_depth(depth, "Skipped copy of %s to %s" % (src, dest))
    else:
        shutil.copy(src, dest)


if __name__ == "__main__":
    inst = InstallData.default()
    # create_dirs(data)
    copy_dirs(0, inst)
