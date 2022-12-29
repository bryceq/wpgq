#!/bin/bash
#read direct

#Add a wallpaper
wpg -a $1

#Auto-adjusts
wpg -A $1

#Sets the wallpaper
wpg -s $1 

#Exports the wallpaper
wpg -o $(wpg -c) ~/current_theme.json

#Restarts Qtile
qtile-cmd -o cmd -f restart

exit
