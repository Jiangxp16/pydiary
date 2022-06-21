import os
import sys
import winreg as reg


def add_to_startup(file_path=None):
    if file_path is None:
        file_path = os.path.abspath(sys.argv[0])
    app = os.path.splitext(os.path.basename(file_path))[0]
    key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as registry_key:
        reg.SetValueEx(registry_key, app, 0, reg.REG_SZ, file_path)
    print("Added to startup")


def remove_from_startup(file_path=None):
    if file_path is None:
        file_path = os.path.abspath(sys.argv[0])
    app = os.path.splitext(os.path.basename(file_path))[0]
    key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as registry_key:
        try:
            reg.DeleteValue(registry_key, app)
        except FileNotFoundError:
            pass
    print("Removed from startup")
