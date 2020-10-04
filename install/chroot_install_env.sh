#!/bin/bash
HOST_NAME="grarch"
USER="gramar"
for i in "$@"
do
case $i in
    -h=*|--host-name=*)
    HOST_NAME="${i#*=}"
    shift # past argument=value
    ;;
    -u=*|--user=*)
    USER="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done


echo "$HOST_NAME" > /etc/hostname
echo "127.0.0.1    localhost" >> /etc/hosts
echo "::1          localhost" >> /etc/hosts


locale-gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
echo "sv_SE.UTF-8 UTF-8" >> /etc/locale.gen
echo "LANG=sv_SE.UTF-8" > /etc/locale.conf

KEYS="se-latin1"
loadkeys $KEYS
echo "KEYMAP=$KEYS" > /etc/vconsole.conf

# set timezone
ln -s /usr/share/zoneinfo/Europe/Stockholm /etc/localtime
timedatectl set-timezone Europe/Stockholm

hwclock --systohc --utc
# Set root pwd
passwd

# make wifi/network work respectively
pacman -S iwd
pacman -S dhcpcd



# Create user
echo "Creating user $USER"
pacman -S sudo --noconfirm
useradd -m "$USER"
passwd "$USER"
echo "$USER    ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
