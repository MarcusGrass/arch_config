#!/bin/bash
# AppArmor
# Add kernel parameters to GRUB_CMDLINE_LINUX_DEFAULT="someparams... apparmor=1 security=apparmor audit=1" in /etc/default/grub
# sudo pacman -S apparmor for userspace tools
# sudo pacman -S audit for auditing
# sudo systemctl enable apparmor
# sudo systemctl enable audit
# reboot
# sudo groupadd -r audit // create audit group
# sudo gpasswd -a gramar audit // add gramar to audit
# sudo vim /etc/audit/auditd.conf // log_group = audit
# mv apparmor-notify.desktop ~/.config/autostart/apparmor-notify.desktop
# reboot
# check that it's working by pgrep -ax aa-notify
# install firejail for internet facing apps
# sudo pacman -S firejail
# sudo apparmor_parser -r /etc/apparmor.d/firejail-default

