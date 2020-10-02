#!/bin/bash
# AppArmor
# Add kernel parameters to GRUB_CMDLINE_LINUX_DEFAULT="someparams... apparmor=1 security=apparmor audit=1" in /etc/default/grub
#  for userspace tools
sudo pacman -S apparmor --noconfirm
#  for auditing
sudo pacman -S audit --noconfirm
sudo systemctl enable apparmor
sudo systemctl enable audit
echo "Reboot then run install/security_two.sh"
