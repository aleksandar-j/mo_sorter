import os
import winreg
import configparser

from tkinter import filedialog
from tkinter import messagebox

class ModOrganizer:

    path = ""

    def __init__(self):
        self.path = self.get_path()

    def is_valid_path(self):
        try:
            for paths, folders, files in os.walk(self.path):
                if "ModOrganizer.exe" in files and \
                        ("mods" in folders or "Mods" in folders) and \
                        ("profiles" in folders or "Profiles" in folders):
                    return True
                else:
                    return False
        except TypeError:
            return False

    def get_path(self):
    
        if self.path:
            return self.path

        try:
            REG_PATH = r"nxm\\shell\\open\\command"

            registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
            value, regtype = winreg.QueryValueEx(registry_key, None)
        
            # We expect the format to be - '"C:\...\nxmhandler.exe" "%x"'
            self.path = value.split("\"")[1]
            # nxmhandler.exe is not needed, remove it
            self.path = self.path[:-(len("nxmhandler.exe")):]

            winreg.CloseKey(registry_key)
        except:
            pass

        while not self.is_valid_path():
            self.path = filedialog.askdirectory(title="Select your ModOrganizer folder")

            # If user just closes the dialog, don't ask again, exit
            if (self.path == ""):
                exit()

        return self.path

    def is_valid_profile(self, mo_profile):
        profiles = self.get_profiles(self.path)
        return mo_profile in profiles

    def get_master_profile(self):
        ConfigParser = configparser.SafeConfigParser()
        ConfigParser.add_section("General")

        ConfigParser.read(self.path + "\\ModOrganizer.ini")
        try:
            master_profile = ConfigParser.get("General", "selected_profile")
        except configparser.NoOptionError:
            master_profile = None
    
        return master_profile

    def get_profiles(self): 
        if not self.is_valid_path():
            return []
        profiles = next(os.walk(self.path + "\\profiles"))[1]
        return profiles
