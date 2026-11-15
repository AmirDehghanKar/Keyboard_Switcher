"""
آیکون سینی سیستم (System Tray) (ui/tray.py)

برنامه کنار ساعت ویندوز می‌نشیند و وضعیت فعال/غیرفعال و زبان فعلی را نشان می‌دهد.
راست‌کلیک: توقف موقت، باز کردن پنجره‌ی اصلی، انتخاب پروفایل، خروج.
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSystemTrayIcon, QMenu


def make_badge_icon(text: str, bg_color: str = "#6c5ce7") -> QIcon:
    """آیکون متنی ساده (FA/EN) برای سینی سیستم می‌سازد تا نیازی به فایل تصویر نباشد."""
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(bg_color))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(2, 2, size - 4, size - 4)
    painter.setPen(QColor("white"))
    font = QFont("Segoe UI", 20, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    painter.end()
    return QIcon(pixmap)


class TrayController:
    def __init__(self, app_window, settings):
        self.window = app_window
        self.settings = settings
        self.tray = QSystemTrayIcon(make_badge_icon("EN"))
        self.tray.setToolTip("AltoShift")

        self.menu = QMenu()
        self.toggle_action = self.menu.addAction("توقف موقت")
        self.toggle_action.triggered.connect(self._toggle_enabled)

        self.profile_menu = self.menu.addMenu("پروفایل فعال")
        self._rebuild_profile_menu()

        self.menu.addSeparator()
        open_action = self.menu.addAction("باز کردن پنجره‌ی اصلی")
        open_action.triggered.connect(self._show_window)

        self.menu.addSeparator()
        quit_action = self.menu.addAction("خروج از برنامه")
        quit_action.triggered.connect(self._quit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_activated)
        self.tray.show()
        self._refresh_toggle_label()

    def _rebuild_profile_menu(self):
        self.profile_menu.clear()
        for name in self.settings.profile_names():
            action = self.profile_menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(name == self.settings.active_profile_name)
            action.triggered.connect(lambda checked, n=name: self._switch_profile(n))

    def _switch_profile(self, name: str):
        self.settings.set_active_profile(name)
        self._rebuild_profile_menu()
        if hasattr(self.window, "reload_rules"):
            self.window.reload_rules()

    def _toggle_enabled(self):
        self.settings.general["enabled"] = not self.settings.general["enabled"]
        self.settings.save()
        self._refresh_toggle_label()

    def _refresh_toggle_label(self):
        enabled = self.settings.general["enabled"]
        self.toggle_action.setText("توقف موقت" if enabled else "فعال‌سازی مجدد")

    def _show_window(self):
        self.window.showNormal()
        self.window.activateWindow()

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_window()

    def _quit(self):
        from PySide6.QtWidgets import QApplication
        QApplication.quit()

    def set_language_badge(self, lang_key: str):
        self.tray.setIcon(make_badge_icon(lang_key))
        self.tray.setToolTip(f"AltoShift — {lang_key}")

    def notify(self, title: str, message: str):
        self.tray.showMessage(title, message, QSystemTrayIcon.Information, 2500)