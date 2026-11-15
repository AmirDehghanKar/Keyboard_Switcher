"""
پایش تغییر پنجره‌ی فعال سیستم (core/window_monitor.py)

به‌جای هوک کردن کلیک ماوس، این ماژول با استفاده از SetWinEventHook به رویداد
EVENT_SYSTEM_FOREGROUND گوش می‌دهد؛ یعنی هر بار پنجره‌ی فعال سیستم عوض شود
(با کلیک، Alt+Tab، کلیک روی تسک‌بار و ...) یک کال‌بک فراخوانی می‌شود.

این روش هم کلیک را پوشش می‌دهد، هم سبک‌تر و پایدارتر از هوک کردن ماوس است.
"""

import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.WinDLL("user32", use_last_error=True)

WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_FOREGROUND = 0x0003

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)


def get_process_name_for_window(hwnd) -> str:
    """نام فایل اجرایی (exe) برنامه‌ی صاحب پنجره را برمی‌گرداند."""
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        return psutil.Process(pid.value).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
        return ""


def get_window_title(hwnd) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


class ForegroundWindowMonitor:
    """هر بار پنجره‌ی فعال سیستم تغییر کند، on_change(exe_name, title, hwnd) را صدا می‌زند."""

    def __init__(self, on_change):
        self.on_change = on_change
        self._hook = None
        self._callback_ref = None  # جلوگیری از garbage collection تابع callback

    def _raw_callback(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        if not hwnd:
            return
        exe = get_process_name_for_window(hwnd)
        title = get_window_title(hwnd)
        try:
            self.on_change(exe, title, hwnd)
        except Exception:
            # خطای داخل کال‌بک نباید کل حلقه‌ی رویداد ویندوز را متوقف کند
            pass

    def start(self):
        self._callback_ref = WinEventProcType(self._raw_callback)
        self._hook = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            self._callback_ref,
            0,
            0,
            WINEVENT_OUTOFCONTEXT,
        )
        return self._hook is not None

    def stop(self):
        if self._hook:
            user32.UnhookWinEvent(self._hook)
            self._hook = None

    @staticmethod
    def pump_messages_once():
        """باید به‌صورت دوره‌ای (مثلاً با QTimer) فراخوانی شود تا پیام‌های
        ویندوز پردازش شوند و رویدادهای WinEvent فعال شوند."""
        msg = wintypes.MSG()
        PM_REMOVE = 0x0001
        while user32.PeekMessageW(ctypes.byref(msg), 0, 0, 0, PM_REMOVE):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
