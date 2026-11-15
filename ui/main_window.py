"""
پنجره‌ی اصلی برنامه (ui/main_window.py)

شامل تب‌های:
  - برنامه‌ها: کارت هر برنامه با سوییچ زبان (FA/EN/به‌خاطر بسپار).
    برنامه‌هایی که اینجا تعریف نشده باشند، اصلاً دست‌خورده نمی‌شوند
    (زبان کیبوردشان تغییر نمی‌کند) — پس نیازی به لیست استثنای جداگانه نیست.
  - آمار استفاده: تعداد دفعات تغییر خودکار زبان برای هر برنامه (با نمودار میله‌ای)
  - تنظیمات: اجرای خودکار، تم، میانبر سراسری، زبان رابط، درون‌ریزی/برون‌بری تنظیمات
"""

import os
import sys
import subprocess

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QPainter, QPixmap, QFont, QDesktopServices
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QComboBox, QTabWidget, QListWidget,
    QListWidgetItem, QCheckBox, QFormLayout, QSpinBox, QFileDialog,
    QMessageBox, QInputDialog, QApplication,
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis,
)

from ui.add_app_dialog import AddAppDialog
from ui.title_rules_dialog import TitleRulesDialog
from ui.styles import get_stylesheet
from ui.i18n import tr, layout_direction, get_language
from core import icon_utils
from core.single_instance import release_single_instance_lock


class AppCard(QWidget):
    ICON_SIZE = 36

    def __init__(self, rule: dict, on_lang_changed, on_remove, on_edit_titles):
        super().__init__()
        self.rule = rule
        self.setObjectName("AppCard")
        self.setFixedHeight(76)
        self.setLayoutDirection(layout_direction())  # صریح، چون QScrollArea گاهی وراثت جهت رو درست منتقل نمی‌کنه

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)

        # به‌جای AlignLeading (که وراثتش داخل QScrollArea قابل‌اعتماد نبود)،
        # صریحاً بر اساس زبان فعلی تعیین می‌کنیم: راست‌چین برای فارسی، چپ‌چین برای انگلیسی
        text_align = Qt.AlignRight if get_language() == "fa" else Qt.AlignLeft

        # --- آیکون برنامه ---
        icon_label = QLabel()
        icon_label.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        display_name = rule.get("display_name") or rule["exe"]
        pixmap = icon_utils.get_icon_pixmap(
            rule["exe"], rule.get("exe_path", ""), self.ICON_SIZE
        )
        if pixmap is None or pixmap.isNull():
            pixmap = self._make_fallback_avatar(display_name, self.ICON_SIZE)
        icon_label.setPixmap(pixmap)

        # --- عنوان و exe ---
        text_box = QVBoxLayout()
        title = QLabel(display_name)
        title.setObjectName("CardTitle")
        title.setAlignment(text_align | Qt.AlignVCenter)
        subtitle = QLabel(rule["exe"])
        subtitle.setObjectName("CardSubtitle")
        subtitle.setAlignment(text_align | Qt.AlignVCenter)
        text_box.addWidget(title)
        text_box.addWidget(subtitle)

        # آیکون همیشه اول اضافه می‌شه: Qt در RTL خودش جایش را کنار عنوان
        # (سمت راستِ متن) می‌برد، و در LTR کنار چپ متن — بدون نیاز به کد جدا
        icon_and_text_row = QHBoxLayout()
        icon_and_text_row.setSpacing(10)
        icon_and_text_row.addWidget(icon_label)
        icon_and_text_row.addLayout(text_box, stretch=1)
        layout.addLayout(icon_and_text_row, stretch=1)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem(tr("lang_fa"), "FA")
        self.lang_combo.addItem(tr("lang_en"), "EN")
        self.lang_combo.addItem(tr("lang_remember"), "REMEMBER")
        idx = self.lang_combo.findData(rule.get("lang", "EN"))
        self.lang_combo.setCurrentIndex(max(idx, 0))
        self.lang_combo.currentIndexChanged.connect(
            lambda: on_lang_changed(rule["exe"], self.lang_combo.currentData())
        )
        layout.addWidget(self.lang_combo)

        title_rules_btn = QPushButton(tr("title_rules_btn"))
        title_rules_btn.setObjectName("SecondaryButton")
        title_rules_btn.clicked.connect(lambda: on_edit_titles(rule["exe"]))
        layout.addWidget(title_rules_btn)

        remove_btn = QPushButton(tr("remove_btn"))
        remove_btn.setObjectName("DangerButton")
        remove_btn.clicked.connect(lambda: on_remove(rule["exe"]))
        layout.addWidget(remove_btn)

    @staticmethod
    def _make_fallback_avatar(display_name: str, size: int) -> QPixmap:
        """وقتی نمی‌شه آیکون واقعی رو از exe استخراج کرد، یه آواتار دایره‌ای
        ساده با حرف اول اسم برنامه می‌سازه (همرنگ تم بنفش برنامه)."""
        letter = (display_name.strip()[:1] or "?").upper()

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#6c5ce7"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        painter.setPen(QColor("white"))
        font = QFont("Segoe UI", int(size * 0.42), QFont.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, letter)
        painter.end()

        return pixmap


class MainWindow(QMainWindow):
    def __init__(self, settings, engine):
        super().__init__()
        self.settings = settings
        self.engine = engine  # SwitcherEngine از main.py، برای اعمال فوری تغییرات
        self.tray_controller = None  # بعداً از main.py تنظیم می‌شود

        self.setWindowTitle(tr("app_title"))
        self.resize(760, 620)
        self.setLayoutDirection(layout_direction())
        self.setStyleSheet(get_stylesheet(settings.general["theme"]))

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.tabs.addTab(self._build_apps_tab(), tr("tab_apps"))
        self.tabs.addTab(self._build_stats_tab(), tr("tab_stats"))
        self.tabs.addTab(self._build_settings_tab(), tr("tab_settings"))

        self.reload_rules()

    # ---------------- تب برنامه‌ها ----------------
    def _build_apps_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        top_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(tr("search_apps_placeholder"))
        self.search_edit.textChanged.connect(self.reload_rules)
        top_row.addWidget(self.search_edit)

        add_btn = QPushButton(tr("add_app_btn"))
        add_btn.clicked.connect(self._on_add_app)
        top_row.addWidget(add_btn)
        layout.addLayout(top_row)

        master_row = QHBoxLayout()
        self.master_switch = QCheckBox(tr("master_switch"))
        self.master_switch.setChecked(self.settings.general["enabled"])
        self.master_switch.stateChanged.connect(self._on_master_toggle)
        master_row.addWidget(self.master_switch)
        master_row.addStretch()
        layout.addLayout(master_row)

        # نشانگر زنده‌ی اسم واقعی exe پنجره‌ی فعال — برای برنامه‌هایی مثل CMD،
        # PowerShell و Git Bash که پنجره‌شون در واقع مال یه میزبان دیگه‌ست
        # (مثلاً conhost.exe یا WindowsTerminal.exe یا mintty.exe)، این کمک می‌کنه
        # اسم درست رو پیدا کنی و همونو به لیست اضافه کنی
        self.live_focus_label = QLabel(tr("live_focus_placeholder"))
        self.live_focus_label.setObjectName("LiveFocusLabel")
        self.live_focus_label.setWordWrap(True)
        layout.addWidget(self.live_focus_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.cards_container)
        layout.addWidget(self.scroll)

        return w

    def update_live_focus_label(self, exe: str, title: str):
        """از core.engine.SwitcherEngine صدا زده می‌شه، هر بار پنجره‌ی فعال سیستم
        عوض بشه — حتی اگه قانونی براش تعریف نشده باشه."""
        short_title = (title[:40] + "…") if len(title) > 40 else title
        self.live_focus_label.setText(f"{tr('live_focus_prefix')}{exe}  —  {short_title}")

    def reload_rules(self):
        # پاک کردن کارت‌های قبلی
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        query = getattr(self, "search_edit", None)
        query_text = query.text().lower() if query else ""

        rules = self.settings.rules
        for rule in rules:
            if query_text and query_text not in (rule.get("display_name", "") + rule["exe"]).lower():
                continue
            card = AppCard(
                rule,
                on_lang_changed=self._on_rule_lang_changed,
                on_remove=self._on_rule_removed,
                on_edit_titles=self._on_edit_title_rules,
            )
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

        if self.engine:
            self.engine.reload_rules()

    def _on_add_app(self):
        dialog = AddAppDialog(self)
        if dialog.exec():
            app = dialog.selected_app
            rule = {
                "exe": app["exe"],
                "exe_path": app.get("exe_path", ""),
                "display_name": app["display_name"],
                "lang": dialog.selected_lang,
                "title_rules": [],
            }
            self.settings.upsert_rule(rule)
            self.reload_rules()

    def _on_rule_lang_changed(self, exe: str, lang: str):
        rule = self.settings.find_rule(exe)
        if rule:
            rule["lang"] = lang
            self.settings.save()
            if self.engine:
                self.engine.reload_rules()

    def _on_rule_removed(self, exe: str):
        self.settings.remove_rule(exe)
        self.reload_rules()

    def _on_edit_title_rules(self, exe: str):
        rule = self.settings.find_rule(exe)
        if not rule:
            return
        dialog = TitleRulesDialog(exe, rule.get("title_rules", []), parent=self)
        if dialog.exec():
            rule["title_rules"] = dialog.get_rules()
            self.settings.save()
            if self.engine:
                self.engine.reload_rules()

    def _on_master_toggle(self, state):
        self.settings.general["enabled"] = bool(state)
        self.settings.save()
        if self.tray_controller:
            self.tray_controller._refresh_toggle_label()

    # ---------------- تب آمار ----------------
    def _build_stats_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel(tr("stats_label")))

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(260)
        self.chart_view.setStyleSheet("background: transparent;")
        layout.addWidget(self.chart_view)

        self.stats_list = QListWidget()
        self.stats_list.setMaximumHeight(160)
        layout.addWidget(self.stats_list)

        refresh_btn = QPushButton(tr("refresh_stats_btn"))
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.clicked.connect(self._reload_stats)
        layout.addWidget(refresh_btn)

        self._reload_stats()
        return w

    def _reload_stats(self):
        stats = self.settings.get_stats()
        items = sorted(stats.items(), key=lambda kv: -kv[1])

        # لیست متنی برای دیدن عدد دقیق هر برنامه
        self.stats_list.clear()
        for exe, count in items:
            self.stats_list.addItem(QListWidgetItem(f"{exe}  —  {count} {tr('stats_count_suffix')}"))

        self._update_chart(items[:10])  # فقط ۱۰ برنامه‌ی پراستفاده‌تر برای خوانایی نمودار

    def _update_chart(self, items):
        # رنگ متن/خط‌های نمودار باید بر اساس تمِ فعلی انتخاب بشه، وگرنه توی
        # تم روشن، متن سفید روی زمینه‌ی روشن تقریباً دیده نمی‌شه
        is_dark = self.settings.general.get("theme", "dark") == "dark"
        text_color = "#e8e8ea" if is_dark else "#1d1e20"
        grid_color = "#3a3b3e" if is_dark else "#d3d4d8"
        muted_color = "#9a9ba0" if is_dark else "#6b6c70"

        chart = QChart()
        chart.setBackgroundVisible(False)
        chart.legend().hide()
        chart.setAnimationOptions(QChart.SeriesAnimations)

        if not items:
            chart.setTitle(tr("chart_empty_title"))
            chart.setTitleBrush(QColor(muted_color))
            self.chart_view.setChart(chart)
            return

        chart.setTitle(tr("chart_title"))
        chart.setTitleBrush(QColor(text_color))

        bar_set = QBarSet(tr("chart_series_name"))
        bar_set.setColor(QColor("#6c5ce7"))
        bar_set.setBorderColor(QColor("#7d6ff0"))

        categories = []
        max_count = 1
        for exe, count in items:
            bar_set.append(count)
            categories.append(exe)
            max_count = max(max_count, count)

        series = QBarSeries()
        series.append(bar_set)
        series.setBarWidth(0.55)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor(text_color))
        axis_x.setGridLineColor(QColor(grid_color))
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor(text_color))
        axis_y.setGridLineColor(QColor(grid_color))
        axis_y.setRange(0, max_count + 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)

    # ---------------- تب تنظیمات ----------------
    def _build_settings_tab(self) -> QWidget:
        w = QWidget()
        layout = QFormLayout(w)

        self.startup_check = QCheckBox()
        self.startup_check.setChecked(self.settings.general["run_on_startup"])
        self.startup_check.stateChanged.connect(
            lambda v: self._update_general("run_on_startup", bool(v))
        )
        layout.addRow(tr("settings_run_on_startup"), self.startup_check)

        self.minimized_check = QCheckBox()
        self.minimized_check.setChecked(self.settings.general["start_minimized"])
        self.minimized_check.stateChanged.connect(
            lambda v: self._update_general("start_minimized", bool(v))
        )
        layout.addRow(tr("settings_start_minimized"), self.minimized_check)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("theme_dark"), "dark")
        self.theme_combo.addItem(tr("theme_light"), "light")
        self.theme_combo.setCurrentIndex(0 if self.settings.general["theme"] == "dark" else 1)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        layout.addRow(tr("settings_theme"), self.theme_combo)

        # زبان رابط کاربری برنامه (نیاز به ریستارت دارد)
        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem("فارسی", "fa")
        self.ui_lang_combo.addItem("English", "en")
        current_ui_lang = self.settings.general.get("ui_language", "fa")
        idx = self.ui_lang_combo.findData(current_ui_lang)
        self.ui_lang_combo.setCurrentIndex(max(idx, 0))
        self.ui_lang_combo.currentIndexChanged.connect(self._on_ui_language_changed)
        layout.addRow(tr("settings_ui_language"), self.ui_lang_combo)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 1000)
        self.delay_spin.setValue(self.settings.general["switch_delay_ms"])
        self.delay_spin.valueChanged.connect(
            lambda v: self._update_general("switch_delay_ms", v)
        )
        layout.addRow(tr("settings_delay"), self.delay_spin)

        self.hotkey_edit = QLineEdit(self.settings.general["hotkey_toggle"])
        self.hotkey_edit.setPlaceholderText(tr("hotkey_placeholder"))
        self.hotkey_edit.editingFinished.connect(
            lambda: self._update_general("hotkey_toggle", self.hotkey_edit.text().strip())
        )
        layout.addRow(tr("settings_hotkey"), self.hotkey_edit)

        # مدیریت پروفایل‌ها
        profile_row = QHBoxLayout()
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.settings.profile_names())
        self.profile_combo.setCurrentText(self.settings.active_profile_name)
        self.profile_combo.currentTextChanged.connect(self._on_profile_changed)
        profile_row.addWidget(self.profile_combo)

        new_profile_btn = QPushButton(tr("new_profile_btn"))
        new_profile_btn.setObjectName("SecondaryButton")
        new_profile_btn.clicked.connect(self._on_new_profile)
        profile_row.addWidget(new_profile_btn)
        layout.addRow(tr("settings_active_profile"), profile_row)

        # درون‌ریزی / برون‌بری
        io_row = QHBoxLayout()
        export_btn = QPushButton(tr("export_btn"))
        export_btn.setObjectName("SecondaryButton")
        export_btn.clicked.connect(self._on_export)
        import_btn = QPushButton(tr("import_btn"))
        import_btn.setObjectName("SecondaryButton")
        import_btn.clicked.connect(self._on_import)
        io_row.addWidget(export_btn)
        io_row.addWidget(import_btn)
        layout.addRow(tr("settings_backup"), io_row)

        # اطلاعات طراح/برنامه‌نویس + دکمه‌ی ارتباط با ایمیل
        developer_label = QLabel("A.DehghanKar")
        developer_label.setStyleSheet("color: #6c5ce7; font-weight: 900;")
        layout.addRow(tr("settings_developer"), developer_label)

        contact_btn = QPushButton(tr("contact_developer_btn"))
        contact_btn.setObjectName("SecondaryButton")
        contact_btn.clicked.connect(self._on_contact_developer)
        layout.addRow("", contact_btn)

        # ریست کامل برنامه (حذف همه‌ی برنامه‌ها، پروفایل‌ها، قوانین و آمار)
        reset_btn = QPushButton(tr("reset_btn"))
        reset_btn.setObjectName("DangerButton")
        reset_btn.clicked.connect(self._on_full_reset)
        layout.addRow(tr("reset_section_label"), reset_btn)

        return w

    def _on_contact_developer(self):
        gmail_compose_url = "https://mail.google.com/mail/?view=cm&fs=1&to=amirdehghan438@gmail.com"
        QDesktopServices.openUrl(QUrl(gmail_compose_url))

    def _on_full_reset(self):
        confirm = QMessageBox.question(
            self,
            tr("reset_confirm_title"),
            tr("reset_confirm_msg"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        self.settings.reset_to_defaults()
        QMessageBox.information(self, tr("reset_confirm_title"), tr("reset_done_msg"))
        self._restart_app()

    def _update_general(self, key, value):
        self.settings.general[key] = value
        self.settings.save()

    def _on_theme_changed(self):
        theme = self.theme_combo.currentData()
        self._update_general("theme", theme)
        self.setStyleSheet(get_stylesheet(theme))
        if hasattr(self, "chart_view"):
            self._reload_stats()  # تا رنگ متن/خطوط نمودار هم با تم جدید هماهنگ بشه

    def _on_ui_language_changed(self):
        new_lang = self.ui_lang_combo.currentData()
        self._update_general("ui_language", new_lang)
        QMessageBox.information(self, tr("restart_required_title"), tr("restart_required_msg"))
        self._restart_app()

    def _restart_app(self):
        """قفل تک‌نمونه‌ای رو آزاد می‌کنه، یک نمونه‌ی جدید از برنامه رو اجرا می‌کنه،
        و بعد برنامه‌ی فعلی رو کامل می‌بنده — بدون نیاز به کار دستی کاربر."""
        release_single_instance_lock()

        if getattr(sys, "frozen", False):
            # نسخه‌ی exe ساخته‌شده با PyInstaller
            cmd = [sys.executable]
            workdir = os.path.dirname(sys.executable)
        else:
            # اجرا با py main.py در حالت توسعه
            script_path = os.path.abspath(sys.argv[0])
            cmd = [sys.executable, script_path]
            workdir = os.path.dirname(script_path)

        subprocess.Popen(cmd, cwd=workdir, close_fds=True)

        # بستن کامل برنامه‌ی فعلی (همون‌قدر تمیز که خروج از منوی سینی سیستم عمل می‌کنه)
        QApplication.quit()

    def _on_profile_changed(self, name: str):
        self.settings.set_active_profile(name)
        self.reload_rules()
        if self.tray_controller:
            self.tray_controller._rebuild_profile_menu()

    def _on_new_profile(self):
        name, ok = QInputDialog.getText(self, tr("new_profile_title"), tr("new_profile_label"))
        if ok and name.strip():
            self.settings.add_profile(name.strip())
            self.profile_combo.addItem(name.strip())
            self.profile_combo.setCurrentText(name.strip())
            if self.tray_controller:
                self.tray_controller._rebuild_profile_menu()

    def _on_export(self):
        path, _ = QFileDialog.getSaveFileName(self, tr("save_settings_title"), "settings_backup.json", "JSON (*.json)")
        if path:
            self.settings.export_to(path)
            QMessageBox.information(self, tr("success_title"), tr("export_success_msg"))

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("load_settings_title"), "", "JSON (*.json)")
        if path:
            self.settings.import_from(path)
            self.reload_rules()
            QMessageBox.information(self, tr("success_title"), tr("import_success_msg"))

    def closeEvent(self, event):
        # به‌جای بستن کامل، پنجره را به سینی سیستم می‌فرستد
        event.ignore()
        self.hide()