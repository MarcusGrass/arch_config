#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"

fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

setxkbmap se
twm &
xclock -geometry 50x50-1+1 &
# xrandr monitor setup
xrandr --output DVI-I-2-2 --primary --auto --output DP-2-5 --auto --above DVI-I-2-2 --output DVI-I-1 --auto --right-of DVI-I-2-2 --output DP-4 --auto --left-of DVI-I-2-2
google-chrome-stable&
intellij-idea-ultimate-edition&
slack&
evolution&
spotify&
zoom&
pavucontrol&
xscreensaver&
xmobar&
exec xmonad
