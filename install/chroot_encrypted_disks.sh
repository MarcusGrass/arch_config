#!/bin/bash

if [ -z "$1" ]
  then
    echo "First argument missing, should be device name /dev/<name> ex: sda"
    exit 1
fi
if [ -z "$2" ]
  then
    echo "Second argument missing, should be root part /dev/<part_name> ex: sda3"
    exit 1
fi
if [ -z "$3" ]
  then
    echo "Third argument missing, should be swap part /dev/<swap_name> ex: sda4"
    exit 1
fi
if [ -z "$4" ]
  then
    echo "Fourth argument missing, should be home part /dev/<part_name> ex: sda5"
    exit 1
fi
# Add boot deps
pacman -S grub --noconfirm
pacman -S efibootmgr --noconfirm
pacman -S python3 --noconfirm

ROOT_KEY="/root/croot.keyfile"
if [ ! -f "$ROOT_KEY" ];
then
  touch $ROOT_KEY
  dd bs=512 count=4 if=/dev/random of=$ROOT_KEY iflag=fullblock
  chmod 000 $ROOT_KEY
  cryptsetup -v luksAddKey /dev/"$2" $ROOT_KEY
fi

HOME_KEY_DIR="/etc/cryptsetup-keys.d"
HOME_KEY="$HOME_KEY_DIR/home.key"
if [ ! -f "$HOME_KEY" ]; then
  mkdir HOME_KEY_DIR
  touch $HOME_KEY
  dd bs=512 count=4 if=/dev/random of=$HOME_KEY iflag=fullblock
  chmod 000 $HOME_KEY
  cryptsetup -v luksAddKey /dev/"$4" $HOME_KEY
fi

LSBLK_OUT=$(lsblk -f)
python3 -m pythonmiscscripts.fix_crypt_conf -in="$LSBLK_OUT" -ckf="$ROOT_KEY" -hkf="$HOME_KEY" -rp="$2" -sp="$3" -hp="$4" \
 && grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB --recheck \
 && grub-install --target=i386-pc --recheck /dev/"$1" \
 && mkinitcpio -P linux \
 && grub-mkconfig -o /boot/grub/grub.cfg
