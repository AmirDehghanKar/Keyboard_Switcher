"""
ثبت میانبر سراسری سیستم (core/hotkey.py)

برای فعال/غیرفعال کردن موقت کل برنامه با یک کلید ترکیبی سراسری
(مثل Ctrl+Alt+K) حتی وقتی پنجره‌ی برنامه فوکوس ندارد.
"""

import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

WM_HOTKEY = 0x0312

HOTKEY_ID = 1

_VK_MAP = {chr(c): c for c in range(0x30, 0x5B)}  # 0-9 و A-Z


def parse_hotkey(text: str):
    """رشته‌ای مثل 'ctrl+alt+k' را به (modifiers, vk_code) تبدیل می‌کند."""
    parts = [p.strip().lower() for p in text.split("+") if p.strip()]
    mods = 0
    vk = None
    for p in parts:
        if p == "ctrl":
            mods |= MOD_CONTROL
        elif p == "alt":
            mods |= MOD_ALT
        elif p == "shift":
            mods |= MOD_SHIFT
        elif p == "win":
            mods |= MOD_WIN
        else:
            vk = _VK_MAP.get(p.upper())
    return mods, vk


class GlobalHotkey:
    def __init__(self, hotkey_text: str, on_trigger):
        self.on_trigger = on_trigger
        self.hotkey_text = hotkey_text
        self._registered = False

    def register(self) -> bool:
        mods, vk = parse_hotkey(self.hotkey_text)
        if vk is None:
            return False
        self._registered = bool(user32.RegisterHotKey(None, HOTKEY_ID, mods, vk))
        return self._registered

    def unregister(self):
        if self._registered:
            user32.UnregisterHotKey(None, HOTKEY_ID)
            self._registered = False

    def pump_messages_once(self):
        """باید دوره‌ای فراخوانی شود (مثلاً با QTimer) تا پیام WM_HOTKEY دریافت شود."""
        msg = wintypes.MSG()
        PM_REMOVE = 0x0001
        while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE):
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                try:
                    self.on_trigger()
                except Exception:
                    pass
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
