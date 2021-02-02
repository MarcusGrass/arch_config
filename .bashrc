#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export VISUAL=vim
export EDITOR="$VISUAL"
shopt -s cdspell
# System
alias off='shutdown -h now'

# Convenience
alias ls='ls --color=auto'
alias endx='python /home/gramar/code/arch_config/pythonmiscscripts/kill_x.py'
alias lock='xscreensaver-command -lock'
# alias ssh='. code/arch_config/bash/ssh.sh'
alias ss='maim -s -u | xclip -selection clipboard -t image/png -i'
alias sstatus='sudo systemctl status'
alias srestart='sudo systemctl restart'
alias startapps='~/code/arch_config/bash/start_apps.sh'

# Vpn
alias vpn_dc='/opt/cisco/anyconnect/bin/vpn disconnect'
alias vpnui='sudo /opt/cisco/anyconnect/bin/vpnui'

# Vpn, if this isn't locked the vpn bugs out to max CPU
alias lock_resolv='sudo chattr +i /etc/resolv.conf'
alias unlock_resolv='sudo chattr -i /etc/resolv.conf && sudo systemctl restart dhcpcd'

# Bluetooth
alias bt='sudo bluetoothctl'
alias bt_re='sudo /bin/bash /home/gramar/code/arch_config/bash/bt_clear.sh'
alias bt_con='sudo bluetoothctl -- connect 4C:87:5D:2C:57:6A && sleep 2 && sudo bluetoothctl -- connect 4C:87:5D:2C:57:6A'
alias bt_dc='sudo bluetoothctl -- disconnect 4C:87:5D:2C:57:6A'


# Git
alias git_reset_master='git fetch origin && git reset --hard origin/master'
alias git_rebase_master='git fetch origin && git rebase -i origin/master'

# Java
alias j11='sudo archlinux-java set java-11-openjdk'
alias j8='sudo archlinux-java set java-8-openjdk'
alias mci='mvn clean install'
alias mcc='mvn clean compile'
alias mgs='mvn generate-sources'

# Idk what this is, probably shouldn't remove
PS1='[\u@\h \W]\$ '
