"""
نقطه‌ی شروع برنامه (main.py)

این فایل تمام بخش‌ها را به هم وصل می‌کند:
  core.settings    -> خواندن/نوشتن تنظیمات
  core.engine      -> موتور تشخیص پنجره‌ی فعال و تغییر زبان
  core.hotkey      -> میانبر سراسری فعال/غیرفعال‌سازی
  core.startup     -> ثبت در Run ویندوز
  ui.main_window   -> پنجره‌ی اصلی (کارت‌ها، تنظیمات، استثناها، آمار)
  ui.tray          -> آیکون سینی سیستم
  ui.osd           -> نمایش کوتاه گوشه‌ی صفحه هنگام تغییر زبان

اجرا:
    python main.py
"""

import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QAbstractNativeEventFilter, Qt
from PySide6.QtGui import QFontDatabase, QIcon

from core.settings import SettingsManager
from core.engine import SwitcherEngine
from core.hotkey import GlobalHotkey, WM_HOTKEY, HOTKEY_ID
from core import startup
from core.fonts import register_fonts
from core.single_instance import acquire_single_instance_lock, notify_already_running
from ui import i18n
from ui.i18n import tr
from ui.main_window import MainWindow
from ui.tray import TrayController
from ui.osd import OSDNotifier


def _resource_path(*parts) -> str:
    """مسیر یک فایل داخل پروژه را هم در حالت توسعه (py main.py) و هم در حالت
    exe ساخته‌شده با PyInstaller درست برمی‌گرداند."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


class HotkeyEventFilter(QAbstractNativeEventFilter):
    """پیام WM_HOTKEY ویندوز را از حلقه‌ی رویداد Qt می‌گیرد و به کال‌بک می‌دهد
    بدون این‌که با پیام‌رسانی داخلی Qt تداخلی ایجاد شود."""

    def __init__(self, on_hotkey):
        super().__init__()
        self.on_hotkey = on_hotkey

    def nativeEventFilter(self, event_type, message):
        try:
            import ctypes
            from ctypes import wintypes

            msg = ctypes.cast(int(message), ctypes.POINTER(wintypes.MSG)).contents
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                self.on_hotkey()
        except Exception:
            pass
        return False, 0


def main():
    # جلوگیری از اجرای همزمان چند نمونه از برنامه
    if not acquire_single_instance_lock():
        notify_already_running()
        sys.exit(0)

    # تنظیمات باید قبل از QApplication خونده بشه تا بدونیم زبان رابط چیه
    settings = SettingsManager()
    i18n.set_language(settings.general.get("ui_language", "fa"))

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setLayoutDirection(i18n.layout_direction())

    # لوگوی برنامه (برای پنجره، تسک‌بار، و Alt+Tab)
    icon_path = _resource_path("assets", "icon.png")
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # بارگذاری فونت‌های Sahel-Light و Sahel-Black از پوشه‌ی fonts/
    # (قبل از ساخت هر پنجره‌ای انجام شود تا استایل‌ها از همان ابتدا اعمال شوند)
    register_fonts()

    # همگام‌سازی گزینه‌ی اجرای خودکار با وضعیت واقعی رجیستری
    startup.set_run_on_startup(settings.general["run_on_startup"])

    osd = OSDNotifier()

    def on_language_switched(lang_key: str):
        osd.show_language(lang_key)
        tray.set_language_badge(lang_key)

    engine = SwitcherEngine(settings, on_language_switched=on_language_switched)

    window = MainWindow(settings, engine)
    engine.on_window_focused = window.update_live_focus_label  # برای نشانگر زنده‌ی exe

    tray = TrayController(window, settings)
    window.tray_controller = tray

    # میانبر سراسری برای فعال/غیرفعال کردن سریع برنامه
    def toggle_enabled_via_hotkey():
        settings.general["enabled"] = not settings.general["enabled"]
        settings.save()
        tray._refresh_toggle_label()
        tray.notify(
            "AltoShift",
            tr("tray_enabled_notify") if settings.general["enabled"] else tr("tray_disabled_notify"),
        )

    hotkey = GlobalHotkey(settings.general["hotkey_toggle"], toggle_enabled_via_hotkey)
    hotkey.register()

    event_filter = HotkeyEventFilter(toggle_enabled_via_hotkey)
    app.installNativeEventFilter(event_filter)

    engine.start()

    if settings.general.get("start_minimized"):
        tray.notify("AltoShift", tr("tray_running_background"))
    else:
        window.show()

    exit_code = app.exec()

    engine.stop()
    hotkey.unregister()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()