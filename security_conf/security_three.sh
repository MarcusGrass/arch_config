#!/bin/bash
# check that it's working by pgrep -ax aa-notify
# install firejail for internet facing apps
sudo pacman -S firejail --noconfirm
sudo apparmor_parser -r /etc/apparmor.d/firejail-default
