"""
دیالوگ افزودن برنامه (ui/add_app_dialog.py)

سه روش برای انتخاب برنامه فراهم می‌کند:
  تب ۱: برنامه‌های نصب‌شده (از روی میانبرهای Start Menu)
  تب ۲: برنامه‌های در حال اجرا
  تب ۳: انتخاب دستی فایل exe

در پایین، زبان مقصد (FA/EN) برای برنامه‌ی انتخاب‌شده تعیین می‌شود.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QComboBox,
    QFileDialog, QMessageBox,
)

from core import app_registry
from ui.i18n import tr, layout_direction


class AddAppDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("add_dialog_title"))
        self.setMinimumSize(460, 480)
        self.setLayoutDirection(layout_direction())

        self.selected_app = None  # dict: display_name, exe_path, exe

        root = QVBoxLayout(self)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.tabs.addTab(self._build_installed_tab(), tr("tab_installed"))
        self.tabs.addTab(self._build_running_tab(), tr("tab_running"))
        self.tabs.addTab(self._build_manual_tab(), tr("tab_manual"))

        # بخش انتخاب زبان
        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel(tr("target_lang_label")))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(tr("lang_fa"), "FA")
        self.lang_combo.addItem(tr("lang_en"), "EN")
        self.lang_combo.addItem(tr("lang_remember_full"), "REMEMBER")
        lang_row.addWidget(self.lang_combo)
        lang_row.addStretch()
        root.addLayout(lang_row)

        # دکمه‌های پایین
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton(tr("cancel_btn"))
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)
        add_btn = QPushButton(tr("add_btn"))
        add_btn.clicked.connect(self._on_add_clicked)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(add_btn)
        root.addLayout(btn_row)

    # ---------- تب برنامه‌های نصب‌شده ----------
    def _build_installed_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        search = QLineEdit()
        search.setPlaceholderText(tr("search_app_placeholder"))
        layout.addWidget(search)

        self.installed_list = QListWidget()
        layout.addWidget(self.installed_list)

        apps = app_registry.list_installed_apps()
        self._populate_list(self.installed_list, apps)

        search.textChanged.connect(
            lambda text: self._populate_list(
                self.installed_list,
                [a for a in apps if text.lower() in a["display_name"].lower()],
            )
        )
        return w

    # ---------- تب در حال اجرا ----------
    def _build_running_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        refresh_btn = QPushButton(tr("refresh_list_btn"))
        refresh_btn.setObjectName("SecondaryButton")
        layout.addWidget(refresh_btn)

        self.running_list = QListWidget()
        layout.addWidget(self.running_list)

        def refresh():
            apps = app_registry.list_running_apps()
            self._populate_list(self.running_list, apps)

        refresh_btn.clicked.connect(refresh)
        refresh()
        return w

    # ---------- تب انتخاب دستی ----------
    def _build_manual_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel(tr("manual_file_label")))

        row = QHBoxLayout()
        self.manual_path_edit = QLineEdit()
        self.manual_path_edit.setReadOnly(True)
        browse_btn = QPushButton(tr("browse_btn"))
        browse_btn.setObjectName("SecondaryButton")
        row.addWidget(self.manual_path_edit)
        row.addWidget(browse_btn)
        layout.addLayout(row)
        layout.addStretch()

        def browse():
            path, _ = QFileDialog.getOpenFileName(
                self, tr("choose_exe_title"), "", "Executable (*.exe)"
            )
            if path:
                self.manual_path_edit.setText(path)
                self._manual_app = app_registry.resolve_manual_exe(path)

        browse_btn.clicked.connect(browse)
        self._manual_app = None
        return w

    # ---------- کمکی‌ها ----------
    def _populate_list(self, list_widget: QListWidget, apps: list):
        list_widget.clear()
        for app in apps:
            item = QListWidgetItem(f"{app['display_name']}   ({app['exe']})")
            item.setData(Qt.UserRole, app)
            list_widget.addItem(item)

    def _on_add_clicked(self):
        current_tab = self.tabs.currentIndex()
        app = None
        if current_tab == 0:
            item = self.installed_list.currentItem()
            app = item.data(Qt.UserRole) if item else None
        elif current_tab == 1:
            item = self.running_list.currentItem()
            app = item.data(Qt.UserRole) if item else None
        else:
            app = self._manual_app

        if not app:
            QMessageBox.warning(self, tr("error_title"), tr("select_app_error"))
            return

        self.selected_app = app
        self.selected_lang = self.lang_combo.currentData()
        self.accept()