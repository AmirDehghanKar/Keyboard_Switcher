"""
بارگذاری فونت‌های همراه برنامه (core/fonts.py)

فونت‌های Sahel-Light.ttf و Sahel-Black.ttf داخل پوشه‌ی fonts/ قرار دارند
و در زمان اجرا (بدون نیاز به نصب روی ویندوز) به Qt معرفی می‌شوند.
هر دو فایل زیر یک خانواده‌ی فونت به اسم "Sahel" ثبت می‌شوند؛ وزن سبک (Light)
و توپر (Black) بعداً در فایل استایل (ui/styles.py) با font-weight انتخاب می‌شود.
"""

import os
import sys
from PySide6.QtGui import QFontDatabase


def _project_root() -> str:
    """وقتی برنامه با PyInstaller به exe تبدیل شده باشد، فایل‌های داده
    (مثل فونت‌ها) در sys._MEIPASS (حالت onefile) یا کنار خود exe قرار دارند،
    نه در مسیر سورس پایتون؛ این تابع هر دو حالت را پوشش می‌دهد."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


FONTS_DIR = os.path.join(_project_root(), "fonts")

FONT_FILES = ["Sahel-Light.ttf", "Sahel-Black.ttf"]


def register_fonts() -> list[str]:
    """فایل‌های فونت را به Qt معرفی می‌کند و نام خانواده‌های ثبت‌شده را برمی‌گرداند.

    اگر فایلی پیدا نشود، بی‌سروصدا رد می‌شود (برنامه با فونت پیش‌فرض سیستم ادامه می‌دهد)
    تا نبودن فونت باعث کرش برنامه نشود.
    """
    registered_families = set()

    if not os.path.isdir(FONTS_DIR):
        return []

    for file_name in FONT_FILES:
        path = os.path.join(FONTS_DIR, file_name)
        if not os.path.isfile(path):
            print(f"[fonts] فایل فونت پیدا نشد: {path}")
            continue

        font_id = QFontDatabase.addApplicationFont(path)
        if font_id == -1:
            print(f"[fonts] بارگذاری فونت ناموفق بود: {file_name}")
            continue

        families = QFontDatabase.applicationFontFamilies(font_id)
        for family in families:
            registered_families.add(family)

    return sorted(registered_families)
