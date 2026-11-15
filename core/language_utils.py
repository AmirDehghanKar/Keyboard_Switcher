"""
ابزارهای کار با چیدمان‌های کیبورد ویندوز (core/language_utils.py)

مسئولیت این ماژول:
  - خواندن لیست چیدمان‌های کیبورد نصب‌شده روی سیستم
  - تشخیص چیدمان فعلی یک پنجره
  - تغییر چیدمان کیبورد یک پنجره‌ی مشخص
"""

import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)

WM_INPUTLANGCHANGEREQUEST = 0x0050
KLF_ACTIVATE = 0x00000001

# شناسه‌ی زبان‌های پرکاربرد (LANGID) -> کد زبان ویندوزی (hex string)
LANGUAGE_PRESETS = {
    "EN": "00000409",  # English (United States)
    "FA": "00000429",  # Persian
    "AR": "00000401",  # Arabic (Saudi Arabia)
    "DE": "00000407",  # German
    "FR": "0000040C",  # French
    "RU": "00000419",  # Russian
    "TR": "0000041F",  # Turkish
}


def get_installed_layouts():
    """چیدمان‌های کیبورد نصب‌شده روی ویندوز را برمی‌گرداند.

    خروجی: لیستی از (hkl_int, lang_tag) مثل [(67699721, '0409'), ...]
    """
    count = user32.GetKeyboardLayoutList(0, None)
    buf = (wintypes.HKL * count)()
    user32.GetKeyboardLayoutList(count, buf)
    layouts = []
    for hkl in buf:
        raw = ctypes.cast(hkl, ctypes.c_void_p).value or 0
        lang_id = raw & 0xFFFF
        layouts.append((raw, f"{lang_id:04x}"))
    return layouts


def is_language_installed(lang_code_hex: str) -> bool:
    """بررسی می‌کند آیا زبان با کد مشخص (مثل '0429' برای فارسی) نصب است."""
    target = lang_code_hex.lower().lstrip("0") or "0"
    for _, tag in get_installed_layouts():
        if tag.lower().lstrip("0") == target:
            return True
    return False


def load_layout(lang_code_full_hex: str):
    """چیدمان را (در صورت نیاز) بارگذاری کرده و شناسه‌ی HKL آن را برمی‌گرداند."""
    return user32.LoadKeyboardLayoutW(lang_code_full_hex, KLF_ACTIVATE)


def get_foreground_window():
    return user32.GetForegroundWindow()


def get_window_thread_and_current_layout(hwnd):
    """شناسه‌ی ترد پنجره و چیدمان کیبورد فعلی آن ترد را برمی‌گرداند."""
    pid = wintypes.DWORD()
    tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    hkl = user32.GetKeyboardLayout(tid)
    lang_id = ctypes.cast(hkl, ctypes.c_void_p).value or 0
    return tid, (lang_id & 0xFFFF)


def set_window_language(hwnd, lang_key: str) -> bool:
    """زبان کیبورد یک پنجره‌ی مشخص را به lang_key (مثل 'FA' یا 'EN') تغییر می‌دهد.

    از دو روش استفاده می‌شود تا سازگاری با بیشتر برنامه‌ها حفظ شود:
      ۱) ارسال پیام WM_INPUTLANGCHANGEREQUEST به خود پنجره
      ۲) فراخوانی مستقیم ActivateKeyboardLayout برای ترد پنجره
    """
    full_hex = LANGUAGE_PRESETS.get(lang_key)
    if not full_hex:
        return False

    hkl = load_layout(full_hex)
    if not hkl:
        return False

    # روش ۱: پیام استاندارد ویندوز (اکثر برنامه‌های win32 و الکترونی را پوشش می‌دهد)
    user32.PostMessageW(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, hkl)

    # روش ۲: فعال‌سازی مستقیم روی ترد پنجره (برای برنامه‌هایی که پیام بالا را نادیده می‌گیرند)
    pid = wintypes.DWORD()
    tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if tid:
        user32.ActivateKeyboardLayout(hkl, KLF_ACTIVATE)

    return True


def current_language_key(hwnd) -> str:
    """بر اساس چیدمان فعلی پنجره، نزدیک‌ترین کلید زبان (FA/EN/...) را حدس می‌زند."""
    _, lang_id = get_window_thread_and_current_layout(hwnd)
    tag = f"{lang_id:04x}"
    for key, full_hex in LANGUAGE_PRESETS.items():
        if full_hex.lower().endswith(tag.lower()):
            return key
    return "EN"
