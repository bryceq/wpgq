#!/bin/bash
compton --config ~/.config/compton.conf --backend glx --paint-on-overlay --vsync opengl-swc &
dunst &
#feh --bg-scale "$(< "${HOME}/.cache/wal/wal")" &
$HOME/.config/wpg/wp_init.sh &
nm-applet &
