#!/bin/bash
pacman -S node
pacman -S yarn
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
# run Plug 'neoclide/coc.nvim', {'branch': 'release'}
