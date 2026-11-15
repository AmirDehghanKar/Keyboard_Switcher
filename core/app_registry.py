"""
شناسایی برنامه‌های نصب‌شده و در حال اجرا (core/app_registry.py)

سه منبع برای افزودن برنامه در دیالوگ «افزودن برنامه» استفاده می‌شود:
  ۱) میانبرهای Start Menu (برنامه‌های نصب‌شده)
  ۲) پردازش‌های در حال اجرا (Task Manager مانند)
  ۳) انتخاب دستی فایل exe
"""

import os
import glob
import psutil

try:
    import win32com.client
    _HAS_WIN32COM = True
except ImportError:
    _HAS_WIN32COM = False


def _start_menu_dirs():
    dirs = []
    appdata = os.environ.get("APPDATA")
    programdata = os.environ.get("PROGRAMDATA")
    if appdata:
        dirs.append(os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs"))
    if programdata:
        dirs.append(os.path.join(programdata, r"Microsoft\Windows\Start Menu\Programs"))
    return dirs


def list_installed_apps():
    """با خواندن میانبرهای (.lnk) Start Menu، لیست برنامه‌های نصب‌شده را برمی‌گرداند.

    خروجی: لیستی از دیکشنری {"display_name": ..., "exe_path": ..., "exe": ...}
    """
    results = {}
    if not _HAS_WIN32COM:
        return []

    shell = win32com.client.Dispatch("WScript.Shell")
    for base_dir in _start_menu_dirs():
        if not os.path.isdir(base_dir):
            continue
        for lnk_path in glob.glob(os.path.join(base_dir, "**", "*.lnk"), recursive=True):
            try:
                shortcut = shell.CreateShortCut(lnk_path)
                target = shortcut.Targetpath
                if not target or not target.lower().endswith(".exe"):
                    continue
                exe_name = os.path.basename(target).lower()
                display_name = os.path.splitext(os.path.basename(lnk_path))[0]
                if exe_name not in results:
                    results[exe_name] = {
                        "display_name": display_name,
                        "exe_path": target,
                        "exe": exe_name,
                    }
            except Exception:
                continue
    return sorted(results.values(), key=lambda a: a["display_name"].lower())


def list_running_apps():
    """لیست برنامه‌های در حال اجرا (با پنجره‌ی قابل مشاهده) را برمی‌گرداند."""
    seen = {}
    for proc in psutil.process_iter(attrs=["pid", "name", "exe"]):
        try:
            name = proc.info["name"]
            exe_path = proc.info["exe"] or ""
            if not name or not name.lower().endswith(".exe"):
                continue
            key = name.lower()
            if key not in seen:
                seen[key] = {
                    "display_name": os.path.splitext(name)[0],
                    "exe_path": exe_path,
                    "exe": key,
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(seen.values(), key=lambda a: a["display_name"].lower())


def resolve_manual_exe(path: str):
    """برای حالت انتخاب دستی فایل exe، اطلاعات پایه را برمی‌گرداند."""
    exe_name = os.path.basename(path).lower()
    display_name = os.path.splitext(os.path.basename(path))[0]
    return {"display_name": display_name, "exe_path": path, "exe": exe_name}
