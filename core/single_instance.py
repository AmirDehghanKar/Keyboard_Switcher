"""
جلوگیری از اجرای همزمان چند نمونه از برنامه (core/single_instance.py)

با ساختن یک Mutex با نام ثابت در سطح سیستم‌عامل کار می‌کند؛ اگر این Mutex
از قبل وجود داشته باشد (یعنی یک نمونه از برنامه در حال اجراست)، نمونه‌ی
جدید متوجه می‌شود و باید بسته شود.
"""

import ctypes

ERROR_ALREADY_EXISTS = 183
MUTEX_NAME = "Global\\AltoShift_SingleInstance_Mutex"

_mutex_handle = None  # باید تا پایان عمر برنامه نگه داشته شود، وگرنه آزاد می‌شود


def acquire_single_instance_lock() -> bool:
    """تلاش می‌کند قفل تک‌نمونه‌ای را بگیرد.

    خروجی True یعنی این اولین (و تنها) نمونه‌ی در حال اجراست.
    خروجی False یعنی نمونه‌ی دیگری از قبل در حال اجراست.
    """
    global _mutex_handle
    kernel32 = ctypes.windll.kernel32
    _mutex_handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    last_error = kernel32.GetLastError()
    return last_error != ERROR_ALREADY_EXISTS


def release_single_instance_lock():
    """قفل تک‌نمونه‌ای را زودتر از بسته‌شدن کامل پردازش آزاد می‌کند؛
    لازم است قبل از اجرای یک نمونه‌ی جدید از برنامه (مثلاً هنگام ریستارت خودکار)
    صدا زده شود، وگرنه نمونه‌ی جدید فکر می‌کند برنامه از قبل در حال اجراست."""
    global _mutex_handle
    if _mutex_handle:
        ctypes.windll.kernel32.CloseHandle(_mutex_handle)
        _mutex_handle = None


def notify_already_running():
    """یک پیام ساده (بدون نیاز به QApplication) به کاربر نشان می‌دهد."""
    MB_ICONINFORMATION = 0x40
    ctypes.windll.user32.MessageBoxW(
        None,
        "برنامه‌ی «AltoShift» از قبل در حال اجراست.\n"
        "آیکون آن را در سینی سیستم (کنار ساعت) پیدا کنید.",
        "در حال اجراست",
        MB_ICONINFORMATION,
    )