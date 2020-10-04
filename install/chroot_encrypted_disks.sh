#!/bin/bash

pacman -S grub --noconfirm
pacman -S efibootmgr --noconfirm
pacman -S python3 --noconfirm

ROOT_KEY="/root/croot.keyfile"
dd bs=512 count=4 if=/dev/random of=$ROOT_KEY iflag=fullblock
chmod 000 $ROOT_KEY
HOME_KEY="/etc/cryptsetup-keys.d/home.key"
dd bs=512 count=4 if=/dev/random of=$HOME_KEY iflag=fullblock
chmod 000 $HOME_KEY
cryptsetup -v luksAddKey /dev/sda3 $ROOT_KEY
cryptsetup -v luksAddKey /dev/sda5 $HOME_KEY

LSBLK_OUT=$(lsblk -f)
python3 -m pythonmiscscripts.fix_crypt_conf -in="$LSBLK_OUT" -ckf="$ROOT_KEY" -hkf="$HOME_KEY"

grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB --recheck
grub-install --target=i386-pc --recheck /dev/sda
mkinitcpio -P linux
grub-mkconfig -o /boot/grub/grub.cfg
