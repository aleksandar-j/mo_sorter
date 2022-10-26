
import os
import winreg
import configparser
from tkinter import filedialog

def is_valid_path(path):
    try:
        _, folders, files = next(os.walk(path))
        if "ModOrganizer.exe" and \
                ("mods" in folders or "Mods" in folders) and \
                ("profiles" in folders or "Profiles" in folders):
            return True
    except:
        pass
    return False

def get_path():
    """
        Returns valid MO path string
    """

    path = ""

    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"nxm\\shell\\open\\command") as regkey:
            value = winreg.QueryValue(regkey, None)
            path = value.split("\" \"")[0][1:-1] # Format is: '"C:\...\nxmhandler.exe" "%x"'
            path = path[:-len("nxmhandler.exe")] # nxmhandler.exe is not needed, remove it
    except:
        pass

    while not is_valid_path(path):
        path = filedialog.askdirectory(title="Select your ModOrganizer folder")
        if not path: # If user just closes the dialog, don't ask again, exit
            exit()

    return path

def get_profiles(path):
    _, folders, _ = next(os.walk(os.path.join(path, "profiles")))
    return folders

def get_profile_active(path):
    """
        Returns active profile or first profile in list if unable
    """

    profile_active = None

    try:
        ConfigParser = configparser.SafeConfigParser()
        ConfigParser.add_section("General")
        ConfigParser.read(os.path.join(path, "ModOrganizer.ini"))
        profile_active = ConfigParser.get("General", "selected_profile")
    except:
        pass

    profiles = get_profiles(path)
    if not profile_active in profiles:
        profile_active = profiles[0]

    return profile_active
