"""
مدیریت اجرای خودکار برنامه همراه ویندوز (core/startup.py)

با نوشتن/حذف یک مقدار در کلید رجیستری Run کاربر فعلی انجام می‌شود؛
نیازی به دسترسی Administrator ندارد.
"""

import sys
import winreg

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_REG_NAME = "AltoShift"


def _executable_command() -> str:
    # وقتی با PyInstaller به exe تبدیل شود، sys.executable همان فایل نهایی است.
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    return f'"{sys.executable}" "{sys.argv[0]}"'


def set_run_on_startup(enabled: bool):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, APP_REG_NAME, 0, winreg.REG_SZ, _executable_command())
            else:
                try:
                    winreg.DeleteValue(key, APP_REG_NAME)
                except FileNotFoundError:
                    pass
    except OSError:
        pass


def is_run_on_startup_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_REG_NAME)
            return True
    except OSError:
        return False