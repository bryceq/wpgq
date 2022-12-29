# wpgq
Automated system-wide theming based on current desktop wallpapers implimented in Python for Qtile.
Uses wpg to sample colors from the existing system wallpaper and exports them in hexadecimal into a file. Then the script refreshes all system components that can read from this file including Qtile widgets, dmenu, etc.
