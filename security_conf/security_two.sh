#!/bin/bash
sudo groupadd -r audit // create audit group
# add gramar to audit
sudo gpasswd -a gramar audit

# add log_group = audit
sudo echo "log_group = audit" | tee -a /etc/audit/auditd.conf > /dev/null
mv ~/code/arch_config/security_conf/apparmor-notify.desktop ~/.config/autostart/apparmor-notify.desktop

echo "Reboot then run install/security_three.sh"

