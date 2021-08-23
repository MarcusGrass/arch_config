import argparse

from pythonmiscscripts.chroot.fix_crypt_conf import fix_conf
from pythonmiscscripts.chroot.prep_env import prep_env
from pythonmiscscripts.format.printer import print_on_depth
from pythonmiscscripts.globals import ROOT, HOME, SWAP, DISK
from pythonmiscscripts.input_utils.parse_input import request_pass
from pythonmiscscripts.os_io.commands import run_cmd, mkfile, mkdir


def install():
    depth = 0
    print_on_depth(depth, "Starting install script")
    pw = request_pass(depth)

    # Add boot deps
    print_on_depth(depth, "Installing boot deps")
    run_cmd(depth, "pacman -S grub --noconfirm --needed")
    run_cmd(depth, "pacman -S efibootmgr --noconfirm --needed")
    run_cmd(depth, "pacman -S sudo --noconfirm --needed")
    run_cmd(depth, "pacman -S iwd --noconfirm --needed")
    run_cmd(depth, "pacman -S dhcpcd --noconfirm --needed")

    print_on_depth(depth, "Generating root keyfile...")
    root_key_file = "/root/croot.keyfile"
    if mkfile(depth, root_key_file):
        run_cmd(depth, "dd bs=512 count=4 if=/dev/random of=%s iflag=fullblock" % root_key_file).get_or_throw()
        run_cmd(depth, "chmod 000 %s" % root_key_file).get_or_throw()
        run_cmd(depth, "cryptsetup -v luksAddKey %s %s" % (ROOT, root_key_file), piped_input=pw).get_or_throw()

    print_on_depth(depth, "Generating home keyfile...")
    home_key_dir = "/etc/cryptsetup-keys.d"
    mkdir(depth, home_key_dir, 644).get_or_throw()
    home_key_file = "%s/home.key" % home_key_dir
    if mkfile(depth, home_key_file):
        run_cmd(depth, "dd bs=512 count=4 if=/dev/random of=%s iflag=fullblock" % home_key_file).get_or_throw()
        run_cmd(depth, "chmod 000 %s" % home_key_file).get_or_throw()
        run_cmd(depth, "cryptsetup -v luksAddKey %s %s" % (HOME, home_key_file), piped_input=pw).get_or_throw()

    print_on_depth(depth, "Generating swap keyfile...")
    swap_key_file = "%s/swap.key" % home_key_dir
    if mkfile(depth, swap_key_file):
        run_cmd(depth, "dd bs=512 count=4 if=/dev/random of=%s iflag=fullblock" % home_key_file).get_or_throw()
        run_cmd(depth, "chmod 000 %s" % swap_key_file).get_or_throw()
        run_cmd(depth, "cryptsetup -v luksAddKey %s %s" % (SWAP, swap_key_file), piped_input=pw).get_or_throw()
    print_on_depth(depth, "Done generating keyfiles")

    print_on_depth(depth, "Fixing crypt conf")
    fix_conf(root_key_file, home_key_file, swap_key_file, get_lsblk(depth))
    print_on_depth(depth, "Executing grub install")
    run_cmd(depth,
            "grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB --recheck").get_or_throw()
    run_cmd(depth, "grub-install --target=i386-pc --recheck %s" % DISK).get_or_throw()
    print_on_depth(depth, "Executing mkinitcpio")
    run_cmd(depth, "mkinitcpio -P").get_or_throw()
    print_on_depth(depth, "Creating grub cfg")
    run_cmd(depth, "grub-mkconfig -o /boot/grub/grub.cfg").get_or_throw()
    prep_env()
    run_cmd(depth, "mkdir /home/gramar")
    run_cmd(depth, "chown -R gramar /home/gramar")
    run_cmd(depth, "chgrp -R gramar /home/gramar")
    run_cmd(depth, "mv /home/setup/arch_config /home/gramar/code")
    run_cmd(depth, "chown -R gramar /home/gramar/code")
    run_cmd(depth, "chgrp -R gramar /home/gramar/code")
    print_on_depth(depth, "Done, enter root password then exit chroot, umount -a, reboot,"
                          " and run install/user_install.sh")


def get_lsblk(depth: int) -> str:
    return run_cmd(depth, "lsblk -f").get_or_throw()


if __name__ == "__main__":
    install()
