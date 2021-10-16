#!/bin/bash
set -e
# Add boot deps
pacman -S python3 --noconfirm --needed >> /dev/null
python3 -m pythonmiscscripts.chroot.fix_crypt_and_env
passwd
