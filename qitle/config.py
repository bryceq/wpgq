# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

import os
import re
import socket
import subprocess
import pywal

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from wal_color import colors


mod = "mod4"
#terminal = guess_terminal()
terminal = "kitty"

### Functions ###

def backlight(action):
    def f(qtile):
        brightness = int(subprocess.run(['xbacklight', '-get'],
                                        stdout=subprocess.PIPE).stdout)
        if brightness != 1 or action != 'dec':
            if (brightness > 49 and action == 'dec') \
                                or (brightness > 39 and action == 'inc'):
                subprocess.run(['xbacklight', f'-{action}', '10',
                                '-fps', '10'])
            else:
                subprocess.run(['xbacklight', f'-{action}', '1'])
    return f


### KEYS ###

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
    #    desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "r",
       # lazy.spawn("dmenu_run -p 'Run: '"),
       # lazy.spawn("./.dmenu/scripts/dmenwal.sh"),
        lazy.spawn("rofi -show run"),
       desc='Dmenu Run Launcher'
        ),
    Key([mod, "shift"], "Return",
            lazy.spawn("nautilus"),
            ),

    # SPECIAL KEYS #
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -c 0 -q set Master toggle")
    ),
    Key([], 'XF86MonBrightnessUp',   lazy.spawn("brightnessctl s 5%+")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("brightnessctl s 5%-")),
]

### GROUPS ###

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

### LAYOUTS ###

layout_theme = {"border_width": 2,
                "margin": 5,
                "border_focus": colors[3],
                "border_normal": "1D2330"
                }




layouts = [
    layout.Columns(
       # border_focus = "#FFFFF",
       # border_width = 2,
       # border_focus_stack='#DE5571',
        margin = 15,
        font = "Hack",
        ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Hack',
    fontsize=12,
    padding=2,
)
extension_defaults = widget_defaults.copy()

### COLORS ###


### SCREEN / BAR ###

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                        linewidth = 0,
                        padding = 10,

                    ),
               # widget.CurrentLayout(),
                widget.GroupBox(
                    background = colors[0],
                    foreground = colors[7],
                    ),
                widget.Prompt(
                    background = colors[0],
                    foreground = colors[7],
                    ),
                widget.WindowName(
                    background = colors[0],
                    foreground = colors[7],
                    ),
               # widget.Chord(
               #     chords_colors={
               #         'launch': ("#ff0000", "#ffffff"),
               #     },
               #     name_transform=lambda name: name.upper(),
               # ),
               # widget.TextBox("default config", name="default"),
               # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Systray(
                    background = colors[0],
                    ),
                widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[2],
                       padding = 0,
                       fontsize = 45
                       ),
                 widget.TextBox(
                       text = "🌡️",
                       padding = 2,
                       foreground = colors[0],
                       background = colors[2],
                       fontsize = 11
                       ),
                 widget.ThermalSensor(
                       foreground = colors[0],
                       background = colors[2],
                       threshold = 90,
                       padding = 5
                       ),
		widget.TextBox(
                      text = '',
                      background = colors[2],
                      foreground = colors[3],
                      padding = 0,
                      fontsize = 45
                      ),
              widget.TextBox(
                    text = '💡',
                    background = colors[3],
                      ),
              widget.Backlight(
                     backlight_name = 'intel_backlight',
                     change_command = 'brightnessctl -s {0},',
                     background = colors[3],
                     foreground = colors[0],
                      ),
              widget.TextBox(
                      text = '',
                      background = colors[3],
                      foreground = colors[2],
                      padding = 0,
                      fontsize = 45
                      ),
              widget.TextBox(
                      text = '🔈',
                      background = colors[2],
                      ),
              widget.Volume(
                      background = colors[2],
                      foreground = colors[0],
                      padding = 5,
                      ),
                widget.TextBox(
                       text = '',
                       background = colors[2],
                       foreground = colors[3],
                       padding = 0,
                       fontsize = 45
                       ),
                widget.TextBox(
                        text = '⚡',
                        background = colors[3],
                        foregound = colors[0],
                        ),
                widget.BatteryIcon(
                       background = colors[3],
                       foreground = colors[2],
                    ),
                widget.Battery(
                       background = colors[3],
                       foreground = colors[0],
                        ),
                widget.TextBox(
                       text = '',
                       background = colors[3],
                       foreground = colors[2],
                       padding = 0,
                       fontsize = 45
                       ),
                widget.TextBox(
                        text = '🌐',
                        background = colors[2],
                        foreground = colors[0],
                        ),
                widget.Wlan(
                    interface='wlp1s0',
                    background = colors[2],
                    foreground = colors[0],
                    ),
                widget.TextBox(
                       text = '',
                       background = colors[2],
                       foreground = colors[3],
                       padding = 0,
                       fontsize = 45
                       ),
                 widget.TextBox(
                       text = "🔄",
                       padding = 2,
                       foreground = colors[0],
                       background = colors[3],
                       fontsize = 14
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Debian",
                       foreground = colors[0],
                       no_update_string = 'No',
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -e sudo apt update && sudo apt upgrade')},
                       background = colors[3]
                       ),
              widget.TextBox(
                       text = "Updates",
                       padding = 5,
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo apt update && sudo apt upgrade')},
                       foreground = colors[0],
                       background = colors[3]
                       ),
              
              widget.TextBox(
                       text = '',
                       background = colors[3],
                       foreground = colors[2],
                       padding = 0,
                       fontsize = 45
                       ),
                 widget.TextBox(
                      text = '📅',
                      background = colors[2],
                      foregound = colors[0],
                      ),
                widget.Clock(
                    format='%a %m/%d/%Y %I:%M %p',
                    background=colors[2],
                    foreground = colors[0],
                    ),
                widget.TextBox(
                       text = '',
                       background = colors[2],
                       foreground = colors[3],
                       padding = 0,
                       fontsize = 45
                       ),
                widget.QuickExit(
                        background = colors[3],
                        default_text = '[ logout ]',
                        foreground = colors[0],
                        ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
