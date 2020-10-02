#!/bin/bash
# set timezone
timedatectl set-timezone Europe/Stockholm

# Create user gramar
echo "Creating user gramar"
pacman -S sudo --noconfirm
useradd -m gramar
passwd gramar
echo "gramar    ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
