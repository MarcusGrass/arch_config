#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export VISUAL=vim
export EDITOR="$VISUAL"
export TERM=xterm-256color
export PATH="$HOME/.local/bin:$PATH"
shopt -s cdspell
# System
alias off='shutdown -h now'

# Convenience
alias pacman='sudo pacman'
alias ls='ls --color=auto'
alias endx='python /home/gramar/code/arch_config/pythonmiscscripts/kill_x.py'
alias lock='xscreensaver-command -lock'
alias xrec='xmonad --recompile'
alias xedit='vim ~/.xmonad/xmonad.hs'
alias xmore='xmonad --recompile && xmonad --restart'
alias syu='sudo pacman -Syu && xmonad --recompile'
alias xclip='xclip -se c'
# alias ssh='. code/arch_config/bash/ssh.sh'
alias ss='maim -s -u | xclip -selection clipboard -t image/png -i'
alias sstatus='sudo systemctl status'
alias srestart='sudo systemctl restart'
alias startapps='~/code/arch_config/bash/start_apps.sh'

# Vpn
alias vpn_con='/opt/cisco/anyconnect/bin/vpn connect login2.avanza.se'
alias vpn_re='sudo chattr -i /etc/resolv.conf && sudo systemctl restart dhcpcd && sleep 2 && sudo /bin/bash /home/gramar/code/arch_config/bash/vpn.sh -r && sudo chattr +i /etc/resolv.conf'
alias vpn_dc='/opt/cisco/anyconnect/bin/vpn disconnect'
alias vpnui='sudo /opt/cisco/anyconnect/bin/vpnui'

# Vpn, if this isn't locked the vpn bugs out to max CPU
alias lock_resolv='sudo chattr +i /etc/resolv.conf'
alias unlock_resolv='sudo chattr -i /etc/resolv.conf && sudo systemctl restart dhcpcd'

# Bluetooth
alias bt='sudo bluetoothctl'
alias bt_re='sudo /bin/bash /home/gramar/code/arch_config/bash/bt_clear.sh'
alias bt_con='sudo bluetoothctl -- connect 4C:87:5D:2C:57:6A'
alias bt_dc='sudo bluetoothctl -- disconnect 4C:87:5D:2C:57:6A'


# Git
alias git_reset_master='git fetch origin && git reset --hard origin/master'
alias git_rebase_master='git fetch origin && git rebase -i origin/master'
alias git_merge_ff='git merge --ff-only'

# Java
alias j15='sudo archlinux-java set java-15-openjdk'
alias j11='sudo archlinux-java set java-11-openjdk'
alias j8='sudo archlinux-java set java-8-openjdk'
alias mci='mvn clean install'
alias mcc='mvn clean compile'
alias mgs='mvn generate-sources'

# Idk what this is, probably shouldn't remove
PS1='[\u@\h \W]\$ '
