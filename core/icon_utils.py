"""
استخراج آیکون واقعی برنامه‌ها از فایل exe (core/icon_utils.py)

از API سطح پایین ویندوز (ExtractIconEx + DrawIconEx روی یک DIB section ۳۲بیتی)
استفاده می‌کند تا کانال شفافیت (آلفا) آیکون هم درست حفظ شود، نه فقط شکل سیاه‌وسفید.

نتیجه‌ها کش می‌شوند تا هر بار که لیست برنامه‌ها دوباره رسم می‌شود، دوباره از دیسک
خوانده نشوند.
"""

import ctypes
import shutil
from ctypes import wintypes

from PySide6.QtGui import QImage, QPixmap

gdi32 = ctypes.WinDLL("gdi32")
user32 = ctypes.WinDLL("user32")
shell32 = ctypes.WinDLL("shell32")

DI_NORMAL = 0x0003
BI_RGB = 0

_icon_cache: dict[str, QPixmap | None] = {}


class _BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class _BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", _BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]


def _resolve_exe_path(exe_name: str, exe_path: str) -> str:
    if exe_path:
        return exe_path
    # اگه مسیر کامل ذخیره نشده بود (مثلاً برنامه‌هایی که قبل از این قابلیت اضافه شدن)،
    # تلاش می‌کنیم مسیرش رو از PATH سیستم پیدا کنیم
    found = shutil.which(exe_name)
    return found or ""


def _extract_hicon_pixmap(exe_path: str, size: int) -> QPixmap | None:
    try:
        large = (ctypes.c_void_p * 1)()
        count = shell32.ExtractIconExW(exe_path, 0, large, None, 1)
        if count <= 0 or not large[0]:
            return None
        hicon = large[0]

        hdc_screen = user32.GetDC(None)
        hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)

        bmi = _BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(_BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = size
        bmi.bmiHeader.biHeight = -size  # مقدار منفی یعنی تصویر از بالا به پایین (top-down)
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = BI_RGB

        bits_ptr = ctypes.c_void_p()
        hbitmap = gdi32.CreateDIBSection(
            hdc_mem, ctypes.byref(bmi), 0, ctypes.byref(bits_ptr), None, 0
        )
        old_obj = gdi32.SelectObject(hdc_mem, hbitmap)

        user32.DrawIconEx(hdc_mem, 0, 0, hicon, size, size, 0, None, DI_NORMAL)

        buf = ctypes.string_at(bits_ptr, size * size * 4)
        image = QImage(buf, size, size, QImage.Format_ARGB32).copy()
        pixmap = QPixmap.fromImage(image)

        gdi32.SelectObject(hdc_mem, old_obj)
        gdi32.DeleteObject(hbitmap)
        gdi32.DeleteDC(hdc_mem)
        user32.ReleaseDC(None, hdc_screen)
        user32.DestroyIcon(hicon)

        return pixmap
    except Exception:
        return None


def get_icon_pixmap(exe_name: str, exe_path: str = "", size: int = 32) -> QPixmap | None:
    """آیکون exe را برمی‌گرداند (با کش). اگر پیدا نشود، None برمی‌گرداند
    تا رابط کاربری یک آواتار جایگزین نشان دهد."""
    cache_key = f"{exe_name.lower()}::{size}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    resolved_path = _resolve_exe_path(exe_name, exe_path)
    pixmap = _extract_hicon_pixmap(resolved_path, size) if resolved_path else None

    _icon_cache[cache_key] = pixmap
    return pixmap