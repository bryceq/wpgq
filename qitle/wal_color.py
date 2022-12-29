import json
import os
import pywal

home = os.path.expanduser('~')

#with open (home+'/.cache/wal/colors.json','r') as string:
with open (home+'/current_theme.json','r') as string:
    my_dict=json.load(string)

colors=[[str(my_dict['colors']['color0'])],
    [str(my_dict['colors']['color1'])],
    [str(my_dict['colors']['color2'])],
    [str(my_dict['colors']['color3'])],
    [str(my_dict['colors']['color4'])],
    [str(my_dict['colors']['color5'])],
    [str(my_dict['colors']['color6'])],
    [str(my_dict['colors']['color7'])],
    [str(my_dict['colors']['color8'])],
    [str(my_dict['colors']['color9'])],
    [str(my_dict['colors']['color10'])],
    [str(my_dict['colors']['color11'])],
    [str(my_dict['colors']['color12'])],
    [str(my_dict['colors']['color13'])],
    [str(my_dict['colors']['color14'])],
    [str(my_dict['colors']['color15'])]]

print(colors)
