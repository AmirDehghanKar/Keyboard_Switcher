"""
دیالوگ مدیریت قوانین متعدد بر اساس عنوان پنجره (ui/title_rules_dialog.py)

برخلاف قبل که فقط با یک خط متنی (جدا شده با ;) می‌شد قوانین رو نوشت،
این دیالوگ اجازه می‌ده هر قانون رو جدا اضافه یا حذف کنی؛ یعنی مثلاً
برای Chrome هم بتونی «Divar.ir=EN» و هم «ChatGPT=FA» رو همزمان نگه داری،
بدون این‌که با اضافه‌کردن یکی، اون‌یکی پاک بشه.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
)

from ui.i18n import tr, layout_direction


class TitleRulesDialog(QDialog):
    def __init__(self, exe_name: str, title_rules: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{tr('title_rules_dialog_title')} — {exe_name}")
        self.setMinimumSize(440, 420)
        self.setLayoutDirection(layout_direction())

        # یک کپی از قوانین فعلی؛ فقط در صورت زدن «ذخیره» روی رول اصلی اعمال می‌شود
        self.rules = [dict(r) for r in title_rules]

        root = QVBoxLayout(self)

        info = QLabel(tr("title_rules_info"))
        info.setWordWrap(True)
        root.addWidget(info)

        # لیست قوانین موجود
        self.list_widget = QListWidget()
        root.addWidget(self.list_widget)

        remove_btn = QPushButton(tr("remove_rule_btn"))
        remove_btn.setObjectName("DangerButton")
        remove_btn.clicked.connect(self._on_remove_rule)
        root.addWidget(remove_btn)

        # ردیف افزودن قانون جدید
        add_row = QHBoxLayout()
        self.contains_edit = QLineEdit()
        self.contains_edit.setPlaceholderText(tr("rule_contains_placeholder"))
        add_row.addWidget(self.contains_edit, stretch=1)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem(tr("lang_fa"), "FA")
        self.lang_combo.addItem(tr("lang_en"), "EN")
        add_row.addWidget(self.lang_combo)

        add_btn = QPushButton(tr("add_rule_btn"))
        add_btn.clicked.connect(self._on_add_rule)
        add_row.addWidget(add_btn)
        root.addLayout(add_row)
        self.contains_edit.returnPressed.connect(self._on_add_rule)

        # دکمه‌های پایین دیالوگ
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        cancel_btn = QPushButton(tr("cancel_btn"))
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton(tr("save_btn"))
        save_btn.clicked.connect(self.accept)
        bottom_row.addWidget(cancel_btn)
        bottom_row.addWidget(save_btn)
        root.addLayout(bottom_row)

        self._refresh_list()

    def _refresh_list(self):
        self.list_widget.clear()
        for rule in self.rules:
            label = f"{rule['contains']}  →  {rule['lang']}"
            item = QListWidgetItem(label)
            self.list_widget.addItem(item)

    def _on_add_rule(self):
        contains = self.contains_edit.text().strip()
        lang = self.lang_combo.currentData()

        if not contains:
            QMessageBox.warning(self, tr("error_title"), tr("rule_contains_error"))
            return

        # اگر قبلاً قانونی با همین متن بود، به‌جای تکرار، زبانش را به‌روزرسانی کن
        for rule in self.rules:
            if rule["contains"].lower() == contains.lower():
                rule["lang"] = lang
                break
        else:
            self.rules.append({"contains": contains, "lang": lang})

        self.contains_edit.clear()
        self._refresh_list()

    def _on_remove_rule(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            del self.rules[row]
            self._refresh_list()

    def get_rules(self) -> list:
        return self.rules