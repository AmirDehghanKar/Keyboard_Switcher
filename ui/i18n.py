"""
سیستم ساده‌ی ترجمه‌ی رابط کاربری (ui/i18n.py)

همه‌ی متن‌های ثابت برنامه اینجا، زیر دو زبان "fa" و "en" تعریف شده‌اند.
تغییر زبان از تب «تنظیمات» ذخیره می‌شود اما فقط بعد از بستن و باز کردن دوباره‌ی
برنامه اعمال می‌شود (چون پنجره‌ها فقط یک‌بار، در لحظه‌ی ساخت، متن می‌گیرند).
"""

from PySide6.QtCore import Qt

_current_lang = "fa"

TRANSLATIONS = {
    "fa": {
        "app_title": "AltoShift",
        "tab_apps": "برنامه‌ها",
        "tab_stats": "آمار استفاده",
        "tab_settings": "تنظیمات",

        "live_focus_prefix": "پنجره‌ی فعال فعلی: ",
        "live_focus_placeholder": "یکی از برنامه‌ها رو باز و روش کلیک کن تا اسم واقعی exe ش اینجا نشون داده بشه",
        "search_apps_placeholder": "جستجو در برنامه‌های اضافه‌شده...",
        "add_app_btn": "+ افزودن برنامه",
        "master_switch": "فعال‌سازی تغییر خودکار زبان",
        "lang_fa": "فارسی (FA)",
        "lang_en": "English (EN)",
        "lang_remember": "آخرین زبان",
        "title_rules_btn": "قوانین عنوان",
        "remove_btn": "حذف",

        "stats_label": "تعداد دفعاتی که زبان کیبورد برای هر برنامه به‌صورت خودکار تغییر کرده:",
        "refresh_stats_btn": "بروزرسانی آمار",
        "chart_title": "تعداد دفعات تغییر خودکار زبان",
        "chart_empty_title": "هنوز هیچ تغییر زبان خودکاری ثبت نشده است",
        "chart_series_name": "تعداد",
        "stats_count_suffix": "بار",

        "settings_run_on_startup": "اجرای خودکار همراه ویندوز:",
        "settings_start_minimized": "شروع برنامه به‌صورت مینیمایز:",
        "settings_theme": "تم رابط کاربری:",
        "theme_dark": "تیره",
        "theme_light": "روشن",
        "settings_delay": "تأخیر قبل از تغییر زبان (ms):",
        "settings_hotkey": "میانبر سراسری فعال/غیرفعال:",
        "hotkey_placeholder": "مثل: ctrl+alt+k",
        "settings_active_profile": "پروفایل فعال:",
        "new_profile_btn": "+ پروفایل جدید",
        "settings_backup": "پشتیبان‌گیری:",
        "settings_developer": "طراح و برنامه‌نویس:",
        "contact_developer_btn": "✉ ارتباط با طراح",
        "reset_section_label": "ریست کامل برنامه:",
        "reset_btn": "🗑 ریست کامل (حذف همه‌ی تنظیمات)",
        "reset_confirm_title": "تأیید ریست کامل",
        "reset_confirm_msg": (
            "همه‌ی برنامه‌های اضافه‌شده، پروفایل‌ها، قوانین عنوان و آمار استفاده "
            "برای همیشه پاک می‌شن.\nاین کار قابل بازگشت نیست. مطمئنی؟"
        ),
        "reset_done_msg": "تنظیمات ریست شد. برنامه هم‌اکنون به‌طور خودکار بسته و دوباره باز می‌شود.",
        "export_btn": "برون‌بری تنظیمات...",
        "import_btn": "درون‌ریزی تنظیمات...",
        "settings_ui_language": "زبان رابط برنامه:",
        "restart_required_title": "اعمال تغییر زبان",
        "restart_required_msg": "زبان رابط برنامه تغییر کرد. برنامه هم‌اکنون به‌طور خودکار بسته و دوباره باز می‌شود.",

        "new_profile_title": "پروفایل جدید",
        "new_profile_label": "نام پروفایل:",
        "save_settings_title": "ذخیره تنظیمات",
        "load_settings_title": "بارگذاری تنظیمات",
        "success_title": "موفق",
        "export_success_msg": "تنظیمات با موفقیت ذخیره شد.",
        "import_success_msg": "تنظیمات با موفقیت بارگذاری شد. لطفاً برنامه را مجدداً باز کنید.",

        "add_dialog_title": "افزودن برنامه",
        "tab_installed": "برنامه‌های نصب‌شده",
        "tab_running": "در حال اجرا",
        "tab_manual": "انتخاب دستی فایل",
        "search_app_placeholder": "جستجوی برنامه...",
        "refresh_list_btn": "🔄 بروزرسانی لیست",
        "manual_file_label": "فایل اجرایی (exe) برنامه‌ی مورد نظر را انتخاب کنید:",
        "browse_btn": "انتخاب فایل...",
        "target_lang_label": "زبان مقصد:",
        "lang_remember_full": "به‌خاطر بسپار آخرین زبان",
        "cancel_btn": "انصراف",
        "add_btn": "افزودن",
        "error_title": "خطا",
        "select_app_error": "لطفاً یک برنامه انتخاب کنید.",
        "choose_exe_title": "انتخاب فایل اجرایی",

        "title_rules_dialog_title": "قوانین عنوان پنجره",
        "title_rules_info": (
            "برای این برنامه، بر اساس بخشی از عنوان پنجره (مثلاً نام تب در مرورگر)\n"
            "می‌تونی چند قانون جدا تعریف کنی. هر قانون مستقل از بقیه اعمال می‌شه."
        ),
        "remove_rule_btn": "حذف قانون انتخاب‌شده",
        "rule_contains_placeholder": "بخشی از عنوان، مثل Divar.ir یا ChatGPT",
        "add_rule_btn": "+ افزودن قانون",
        "save_btn": "ذخیره",
        "rule_contains_error": "لطفاً بخشی از عنوان پنجره را وارد کنید.",

        "tray_pause": "توقف موقت",
        "tray_resume": "فعال‌سازی مجدد",
        "tray_active_profile": "پروفایل فعال",
        "tray_open_window": "باز کردن پنجره‌ی اصلی",
        "tray_quit": "خروج از برنامه",
        "tray_enabled_notify": "فعال شد",
        "tray_disabled_notify": "موقتاً غیرفعال شد",
        "tray_running_background": "برنامه در پس‌زمینه در حال اجراست.",
    },
    "en": {
        "app_title": "AltoShift",
        "tab_apps": "Apps",
        "tab_stats": "Usage Stats",
        "tab_settings": "Settings",

        "live_focus_prefix": "Currently focused window: ",
        "live_focus_placeholder": "Open and click on any app to see its real exe name here",
        "search_apps_placeholder": "Search added apps...",
        "add_app_btn": "+ Add App",
        "master_switch": "Enable automatic language switching",
        "lang_fa": "Persian (FA)",
        "lang_en": "English (EN)",
        "lang_remember": "Last language",
        "title_rules_btn": "Title Rules",
        "remove_btn": "Remove",

        "stats_label": "Number of automatic language switches per app:",
        "refresh_stats_btn": "Refresh Stats",
        "chart_title": "Automatic Language Switch Count",
        "chart_empty_title": "No automatic language switches recorded yet",
        "chart_series_name": "Count",
        "stats_count_suffix": "times",

        "settings_run_on_startup": "Run automatically with Windows:",
        "settings_start_minimized": "Start minimized:",
        "settings_theme": "UI Theme:",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "settings_delay": "Delay before switching language (ms):",
        "settings_hotkey": "Global enable/disable hotkey:",
        "hotkey_placeholder": "e.g. ctrl+alt+k",
        "settings_active_profile": "Active profile:",
        "new_profile_btn": "+ New Profile",
        "settings_backup": "Backup:",
        "settings_developer": "Designer & Developer:",
        "contact_developer_btn": "✉ Contact Developer",
        "reset_section_label": "Full app reset:",
        "reset_btn": "🗑 Full Reset (delete all settings)",
        "reset_confirm_title": "Confirm Full Reset",
        "reset_confirm_msg": (
            "All added apps, profiles, title rules and usage stats will be "
            "permanently deleted.\nThis cannot be undone. Are you sure?"
        ),
        "reset_done_msg": "Settings were reset. The app will now close and reopen automatically.",
        "export_btn": "Export settings...",
        "import_btn": "Import settings...",
        "settings_ui_language": "App interface language:",
        "restart_required_title": "Applying language change",
        "restart_required_msg": "The interface language has changed. The app will now close and reopen automatically.",

        "new_profile_title": "New Profile",
        "new_profile_label": "Profile name:",
        "save_settings_title": "Save Settings",
        "load_settings_title": "Load Settings",
        "success_title": "Success",
        "export_success_msg": "Settings were saved successfully.",
        "import_success_msg": "Settings were loaded successfully. Please restart the app.",

        "add_dialog_title": "Add App",
        "tab_installed": "Installed Apps",
        "tab_running": "Running",
        "tab_manual": "Choose File Manually",
        "search_app_placeholder": "Search app...",
        "refresh_list_btn": "🔄 Refresh List",
        "manual_file_label": "Select the executable (exe) file of the app:",
        "browse_btn": "Browse...",
        "target_lang_label": "Target language:",
        "lang_remember_full": "Remember last language",
        "cancel_btn": "Cancel",
        "add_btn": "Add",
        "error_title": "Error",
        "select_app_error": "Please select an app.",
        "choose_exe_title": "Select executable file",

        "title_rules_dialog_title": "Window Title Rules",
        "title_rules_info": (
            "For this app, you can define several separate rules based on part of\n"
            "the window title (e.g. a browser tab name). Each rule applies independently."
        ),
        "remove_rule_btn": "Remove selected rule",
        "rule_contains_placeholder": "Part of the title, e.g. Divar.ir or ChatGPT",
        "add_rule_btn": "+ Add Rule",
        "save_btn": "Save",
        "rule_contains_error": "Please enter part of the window title.",

        "tray_pause": "Pause",
        "tray_resume": "Resume",
        "tray_active_profile": "Active Profile",
        "tray_open_window": "Open Main Window",
        "tray_quit": "Quit",
        "tray_enabled_notify": "Enabled",
        "tray_disabled_notify": "Temporarily disabled",
        "tray_running_background": "The app is running in the background.",
    },
}


def set_language(lang: str):
    """باید فقط یک‌بار و قبل از ساخت هر پنجره‌ای در main.py صدا زده شود."""
    global _current_lang
    _current_lang = lang if lang in TRANSLATIONS else "fa"


def get_language() -> str:
    return _current_lang


def tr(key: str) -> str:
    """متن معادل کلید را در زبان فعلی برمی‌گرداند؛ اگر پیدا نشد، خودِ کلید را برمی‌گرداند."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["fa"]).get(key, key)


def layout_direction():
    """جهت چیدمان مناسب زبان فعلی (راست‌به‌چپ برای فارسی، چپ‌به‌راست برای انگلیسی)."""
    return Qt.RightToLeft if _current_lang == "fa" else Qt.LeftToRight