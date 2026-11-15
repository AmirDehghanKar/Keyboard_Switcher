"""
نمایش کوتاه روی صفحه (On-Screen Display) برای تأیید تغییر زبان (ui/osd.py)

هر بار زبان کیبورد به‌صورت خودکار تغییر کند، یک حباب کوچک و محوشونده
گوشه‌ی پایین راست صفحه نمایش داده می‌شود تا کاربر مطمئن شود عملیات انجام شده.
"""

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication

LABELS = {"FA": "فارسی", "EN": "English"}


class OSDNotifier(QWidget):
    def __init__(self):
        super().__init__(
            None,
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
            | Qt.NoDropShadowWindowHint,
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName("OSDRoot")

        self.container = QWidget(self)
        self.container.setObjectName("OSD")
        self.container.setFixedSize(150, 90)

        layout = QVBoxLayout(self.container)
        self.label = QLabel("FA")
        self.label.setObjectName("OSDLabel")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setFixedSize(150, 90)

        self._effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._effect)
        self._effect.setOpacity(0.0)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._fade_out)

    def _position_bottom_right(self):
        screen: QScreen = QApplication.primaryScreen()
        geo = screen.availableGeometry()
        x = geo.right() - self.width() - 24
        y = geo.bottom() - self.height() - 24
        self.move(x, y)

    def show_language(self, lang_key: str, duration_ms: int = 1100):
        self.label.setText(LABELS.get(lang_key, lang_key))
        self._position_bottom_right()
        self.show()

        self._fade_in = QPropertyAnimation(self._effect, b"opacity")
        self._fade_in.setDuration(140)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)
        self._fade_in.setEasingCurve(QEasingCurve.OutCubic)
        self._fade_in.start()

        self._hide_timer.start(duration_ms)

    def _fade_out(self):
        self._fade_out_anim = QPropertyAnimation(self._effect, b"opacity")
        self._fade_out_anim.setDuration(220)
        self._fade_out_anim.setStartValue(1.0)
        self._fade_out_anim.setEndValue(0.0)
        self._fade_out_anim.setEasingCurve(QEasingCurve.InCubic)
        self._fade_out_anim.finished.connect(self.hide)
        self._fade_out_anim.start()
