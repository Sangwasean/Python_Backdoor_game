# Security Education Cleanup Tool
import winreg as reg
import os

print("Educational Cleanup Tool - Removing Demo Entries")
try:
    key = reg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as reg_key:
        reg.DeleteValue(reg_key, "CyberEducation")
    print("Removed educational persistence entry")
except Exception as e:
    print("Cleanup completed with status:", str(e))
input("Press ENTER to exit...")
