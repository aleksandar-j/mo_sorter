import os
import time

from tkinter import messagebox

my_file_name = "modorganizersorter_modlist.txt"

def overwrite(modlist_current_path, your_modlist_path):
    os.replace(modlist_current_path, your_modlist_path + ".BAK")
    os.replace(your_modlist_path, modlist_current_path)

def equalize(master_profile_path, profile_path):

    # Open master profile modlist
    try:
        mp_file = open(master_profile_path + "\\modlist.txt", 'r')
    except:
        message = """Your master profile is missing mod-list configuration.
                  Please reopen Mod Organizer with desired profile selected"""
        messagebox.showinfo("Info", message)
        exit()

    # Open our profile modlist and read everything
    p_file_path = profile_path + "\\modlist.txt"
        
    p_file_data_signs = []
    p_file_data_mods = []
    try:
        p_file = open(p_file_path, 'r')
        
        p_file.seek(0)
        for line in p_file:
            if line[0] == '-' or line[0] == '+':
                p_file_data_signs.append(line[0])
                p_file_data_mods.append(line[1:])
        
        p_file.close()
    except:
        p_file = open(profile_path + "\\modlist.txt", 'w+')
        
    # Create my_file which is new modlist.txt file in current profile
    my_file_path = profile_path + "\\" + my_file_name
    
    my_file = open(my_file_path, 'w+')

    # Read through master profile and copy into current profile
    mp_file.seek(0)
    for i_mp, line_mp in enumerate(mp_file):
        if line_mp[0] == '-' or line_mp[0] == '+':
            current_mod = line_mp[1:]
            current_sign = '-'

            try:
                i = p_file_data_mods.index(current_mod)
                current_sign = p_file_data_signs[i]
            except ValueError:
                pass

            my_file.write(current_sign + current_mod)
        else:
            my_file.write(line_mp)

    # Close all files
    mp_file.close()
    my_file.close()

    # Backup the old modlist and put our new one in charge
    overwrite(p_file_path, my_file_path)

def sort(mo_path, master_profile, profiles, parent_window):
    if master_profile not in profiles:
        message = "Select valid profile!"
        messagebox.showinfo("Info", message)
        return

    profiles.remove(master_profile)

    for profile in profiles:
        equalize(mo_path + "\\profiles\\" + master_profile, mo_path + "\\profiles\\" + profile)

    profiles.append(master_profile)

    message = "All done!"
    messagebox.showinfo("Info", message)
