#!/bin/bash
BASE_DIR="$HOME/code/arch_config/"
FILES=("/.Xresources" "/.xmonad/xmonad.hs" "/.xscreensaver" "/.xmobarrc" "/.xinitrc" "/.bashrc")
for F in "${FILES[@]}"; do
  mv "$HOME$F" "$HOME$F.bak"
  cp "$BASE_DIR$F" "$HOME$F"
done
