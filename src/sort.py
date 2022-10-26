
import os
import datetime
from tkinter import messagebox

MISSING_MODLIST_TXT = "Your active profile is missing mod-list configuration.\nPlease reopen Mod Organizer with desired profile selected"

def iso_date():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def get_name_active_list(modlist):
    return [(line[1:], line[0]) for line in modlist.split("\n") if line]
def merge_name_active_list(names, actives):
    return [(names[i][0], actives[i][1]) for i in range(len(names))]

def get_modlist(name_active):
    modlist_lines = [active + name for name, active in name_active]
    modlist = '\n'.join(modlist_lines) + '\n'
    return modlist

def read(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None

def sort(mo_path, profile_active, profiles):
    if profile_active not in profiles:
        messagebox.showinfo("Error", "Select valid profile!")
        return

    profiles_path = os.path.join(mo_path, "profiles")
    
    profile_active_modlist_path = os.path.join(profiles_path, profile_active, "modlist.txt")
    profile_active_modlist = read(profile_active_modlist_path)

    if profile_active_modlist is None:
        messagebox.showinfo("Error", MISSING_MODLIST_TXT)
        return

    name_active_src = get_name_active_list(profile_active_modlist)

    for profile in profiles:
        if profile == profile_active:
            continue
        
        profile_modlist_path = os.path.join(profiles_path, profile, "modlist.txt")
        profile_modlist = read(profile_modlist_path)
        if profile_modlist is None:
            profile_modlist = profile_active_modlist

        name_active_dest = get_name_active_list(profile_modlist)
        name_active_dest_new = merge_name_active_list(name_active_src, name_active_dest)
        modlist_dest_new = get_modlist(name_active_dest_new)
        
        os.replace(profile_modlist_path, os.path.join(profiles_path, profile, "modlist.txt." + iso_date() + ".BAK"))
        with open(profile_modlist_path, 'w+') as f:
            f.write(modlist_dest_new)

    messagebox.showinfo("Info", "All done!")
