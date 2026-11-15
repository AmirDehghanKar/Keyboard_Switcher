"""
استایل‌های ظاهری برنامه (ui/styles.py)

دو تم تیره و روشن با گوشه‌های گرد، رنگ‌بندی مدرن شبیه ویندوز ۱۱
و پشتیبانی کامل از راست‌به‌چپ (برای رابط فارسی).
"""

DARK_QSS = """
QWidget {
    background-color: #1e1f22;
    color: #e8e8ea;
    font-family: "Sahel", "Segoe UI", sans-serif;
    font-weight: 300; /* نسخه‌ی سبک (Sahel-Light) برای متن عادی */
    font-size: 14px;
}

QMainWindow, QDialog {
    background-color: #1e1f22;
}

#Sidebar {
    background-color: #17181a;
    border-right: 1px solid #2c2d30;
}

#TopBar {
    background-color: #1e1f22;
    border-bottom: 1px solid #2c2d30;
}

QLineEdit {
    background-color: #2a2b2e;
    border: 1px solid #3a3b3e;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e8e8ea;
}
QLineEdit:focus {
    border: 1px solid #6c5ce7;
}

QPushButton {
    background-color: #6c5ce7;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 900; /* نسخه‌ی توپر (Sahel-Black) برای دکمه‌ها */
}
QPushButton:hover { background-color: #7d6ff0; }
QPushButton:pressed { background-color: #5b4bd6; }
QPushButton:disabled { background-color: #3a3b3e; color: #88898c; }

QPushButton#SecondaryButton {
    background-color: #2a2b2e;
    color: #e8e8ea;
    border: 1px solid #3a3b3e;
}
QPushButton#SecondaryButton:hover { background-color: #34353a; }

QPushButton#DangerButton {
    background-color: transparent;
    color: #ff6b6b;
    border: 1px solid #ff6b6b;
}
QPushButton#DangerButton:hover { background-color: rgba(255,107,107,0.12); }

#AppCard {
    background-color: #28292c;
    border-radius: 14px;
    border: 1px solid #323336;
}
#AppCard:hover { border: 1px solid #6c5ce7; }

#CardTitle { font-size: 15px; font-weight: 900; } /* Sahel-Black */
#CardSubtitle { color: #9a9ba0; font-size: 12px; }
#LiveFocusLabel { color: #6c5ce7; font-size: 12px; font-weight: 900; } /* Sahel-Black */

QComboBox {
    background-color: #2a2b2e;
    border: 1px solid #3a3b3e;
    border-radius: 8px;
    padding: 6px 10px;
    min-width: 90px;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background-color: #2a2b2e;
    selection-background-color: #6c5ce7;
    border-radius: 6px;
}

QListWidget, QScrollArea { border: none; background: transparent; }

QScrollBar:vertical {
    background: #ffffff;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #6c5ce7;
    border-radius: 5px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover { background: #7d6ff0; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0px; }
QScrollBar::add-page, QScrollBar::sub-page { background: none; }

QTabWidget::pane { border: 1px solid #2c2d30; border-radius: 10px; }
QTabBar::tab {
    background: transparent;
    padding: 8px 16px;
    color: #9a9ba0;
}
QTabBar::tab:selected {
    color: #e8e8ea;
    font-weight: 900; /* Sahel-Black */
    border-bottom: 2px solid #6c5ce7;
}

#StatusPill {
    border-radius: 10px;
    padding: 4px 12px;
    font-weight: 900; /* Sahel-Black */
}
#StatusPill[state="on"] { background-color: rgba(76,201,133,0.15); color: #4cc985; }
#StatusPill[state="off"] { background-color: rgba(154,155,160,0.15); color: #9a9ba0; }

QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; }

#OSD {
    background-color: rgba(30, 31, 34, 0.92);
    border: 1px solid #6c5ce7;
    border-radius: 16px;
}
#OSDLabel { font-size: 28px; font-weight: 900; color: #e8e8ea; } /* Sahel-Black */
"""

LIGHT_QSS = DARK_QSS.replace("#1e1f22", "#f5f5f7") \
    .replace("#17181a", "#eceef1") \
    .replace("#2c2d30", "#dcdde1") \
    .replace("#2a2b2e", "#ffffff") \
    .replace("#3a3b3e", "#d3d4d8") \
    .replace("#e8e8ea", "#1d1e20") \
    .replace("#28292c", "#ffffff") \
    .replace("#323336", "#e2e3e6") \
    .replace("#9a9ba0", "#6b6c70") \
    .replace("#34353a", "#eceef1") \
    .replace("rgba(30, 31, 34, 0.92)", "rgba(255, 255, 255, 0.95)")


def get_stylesheet(theme: str) -> str:
    return DARK_QSS if theme == "dark" else LIGHT_QSS