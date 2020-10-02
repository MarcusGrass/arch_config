#!/bin/bash
# Check that the correct user is running
USER=$(whoami)
if [ "$USER" != "gramar" ]; then
	echo "Needs to be run as gramar, you are running as $USER"
	exit 1
fi

# Dhcp
sudo pacman -S dhcpcd --noconfirm

# Time
sudo pacman -S ntp --noconfirm

# Install essentials, gvim for clipboard support etc
sudo pacman -S gvim --noconfirm
sudo pacman -S bash-completion --noconfirm
sudo pacman -S openssl --noconfirm
sudo pacman -S openssh --noconfirm

# Git and generate keys
EMAIL="marcus.grass@gmail.com"
echo "Installing git and generating keys for $EMAIL"
git config --global user.email "${EMAIL}"
git config --global user.name "MarcusGrass"
git config --global pull.rebase true
git config --global push.default current
git config --global rerere.enabled true

ssh-keygen -t rsa -b 4096 -C $EMAIL
ssh-add ~/.ssh/id_rsa
echo "Add the key from ~/.ssh/id_rsa to github to finish git install"

# install xmonad and xterm
sudo pacman -S xorg-server --noconfirm
sudo pacman -S xorg-xinit --noconfirm
sudo pacman -S xterm --noconfirm
sudo pacman -S xrandr --noconfirm
sudo pacman -S xscreensaver --noconfirm

sudo pacman -S xmonad --noconfirm
sudo pacman -S xmonad-contrib --noconfirm
sudo pacman -S xmobar --noconfirm

# Bluetooth and sound
sudo pacman -S pulseaudio --noconfirm
sudo pacman -S pavucontrol --noconfirm
sudo pacman -S pulseaudio-bluetooth --noconfirm
sudo pacman -S pulsemixer --noconfirm
sudo pacman -S bluez --noconfirm
sudo pacman -S bluez-util--noconfirm

# Java
sudo pacman -S jdk11-openjdk --noconfirm
sudo pacman -S openjdk11-src --noconfirm
sudo pacman -S jdk8-openjdk --noconfirm
sudo pacman -S openjdk8-src --noconfirm

#Python
sudo pacman -S python3 --noconfirm

# Rust
sudo pacman -S rustup --noconfirm
rustup toolchain install stable

# Docker
sudo pacman -S docker --noconfirm
sudo pacman -S docker-compose --noconfirm
# Needed for no-sudo docker
sudo groupadd docker
sudo gpasswd -a gramar docker

# Printscreen
sudo pacman -S pinta --noconfirm
sudo pacman -S maim --noconfirm

# Password manager
sudo pacman -S pass --noconfirm

# Email
sudo pacman -S evolution --noconfirm
sudo pacman -S evolution-ews --noconfirm

# Cron
sudo pacman -S cronie --noconfirm


# Create directory structure
mkdir -p ~/pictures/screenshots
mkdir ~/code/java
mkdir ~/code/python
mkdir ~/code/bash
mkdir ~/code/rust
mkdir ~/code/unclassified
mkdir ~/documents
mkdir ~/downloads/
mkdir ~/misc

# Xorg conf
cp -r ~/code/arch_config/.xmonad ~/.xmonad
cp -r ~/code/arch_config/.gnupg ~/.gnupg
cp ~/code/arch_config/.xinitrc ~/.xinitrc
cp ~/code/arch_config/.Xresources ~/.Xresources
cp ~/code/arch_config/.xscreensaver ~/.xscreensaver
cp ~/code/arch_config/.bashrc ~/.bashrc
cp ~/code/arch_config/.xmobarrc ~/.xmobarrc

# Start services
echo "Enabling services now"
sudo systemctl enable --now bluetooth
sudo systemctl enable --now cronie
sudo systemctl enable --now dhcpcd
sudo systemctl enable --now ntpd
pulseaudio --start

# download drivers
echo "Video driver is: $(lspci | grep -e VGA -e 3D)"
echo "Use pacman -Ss xf86-video to find the correct driver then run startx to enter window manager"
