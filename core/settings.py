"""
مدیریت ذخیره و بارگذاری تنظیمات برنامه (core/settings.py)

تمام تنظیمات (قوانین برنامه‌ها، پروفایل‌ها، گزینه‌های عمومی) به صورت
یک فایل JSON در مسیر زیر ذخیره می‌شود:

    %APPDATA%\\KeyboardSwitcher\\settings.json

ساختار داده (نمونه):
{
    "general": {
        "run_on_startup": true,
        "start_minimized": true,
        "theme": "dark",
        "ui_language": "fa",
        "switch_delay_ms": 50,
        "enabled": true,
        "active_profile": "پیش‌فرض",
        "hotkey_toggle": "ctrl+alt+k"
    },
    "profiles": {
        "پیش‌فرض": {
            "rules": [
                {
                    "exe": "chrome.exe",
                    "display_name": "Google Chrome",
                    "lang": "FA",
                    "title_rules": [
                        {"contains": "ChatGPT", "lang": "FA"},
                        {"contains": "GitHub", "lang": "EN"}
                    ],
                    "remember_last": false
                }
            ]
        }
    },
    "last_language": {
        "chrome.exe": "FA"
    },
    "stats": {
        "chrome.exe": 42
    }
}
"""

import json
import os
import copy

APP_DIR_NAME = "AltoShift"
SETTINGS_FILE_NAME = "settings.json"

DEFAULT_SETTINGS = {
    "general": {
        "run_on_startup": False,
        "start_minimized": False,
        "theme": "dark",
        "ui_language": "fa",
        "switch_delay_ms": 50,
        "enabled": True,
        "active_profile": "پیش‌فرض",
        "hotkey_toggle": "ctrl+alt+k",
        "admin_mode": False,
    },
    "profiles": {
        "پیش‌فرض": {
            "rules": [],
        }
    },
    "last_language": {},
    "stats": {},
}


def get_settings_dir() -> str:
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, APP_DIR_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def get_settings_path() -> str:
    return os.path.join(get_settings_dir(), SETTINGS_FILE_NAME)


def _deep_merge(default: dict, loaded: dict) -> dict:
    """مقادیر گمشده در فایل ذخیره‌شده را از مقادیر پیش‌فرض پر می‌کند."""
    result = copy.deepcopy(default)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class SettingsManager:
    def __init__(self):
        self.path = get_settings_path()
        self.data = self.load()

    def load(self) -> dict:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                return _deep_merge(DEFAULT_SETTINGS, loaded)
            except (json.JSONDecodeError, OSError):
                pass
        return copy.deepcopy(DEFAULT_SETTINGS)

    def save(self):
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.path)

    # ---------- general ----------
    @property
    def general(self) -> dict:
        return self.data["general"]

    # ---------- profiles ----------
    @property
    def active_profile_name(self) -> str:
        return self.data["general"]["active_profile"]

    @property
    def active_profile(self) -> dict:
        profiles = self.data["profiles"]
        name = self.active_profile_name
        if name not in profiles:
            name = next(iter(profiles))
            self.data["general"]["active_profile"] = name
        return profiles[name]

    def set_active_profile(self, name: str):
        if name in self.data["profiles"]:
            self.data["general"]["active_profile"] = name
            self.save()

    def add_profile(self, name: str):
        if name and name not in self.data["profiles"]:
            self.data["profiles"][name] = {"rules": []}
            self.save()

    def delete_profile(self, name: str):
        if name in self.data["profiles"] and len(self.data["profiles"]) > 1:
            del self.data["profiles"][name]
            if self.data["general"]["active_profile"] == name:
                self.data["general"]["active_profile"] = next(iter(self.data["profiles"]))
            self.save()

    def profile_names(self):
        return list(self.data["profiles"].keys())

    # ---------- rules ----------
    @property
    def rules(self) -> list:
        return self.active_profile["rules"]

    def find_rule(self, exe: str):
        exe = exe.lower()
        for rule in self.rules:
            if rule["exe"].lower() == exe:
                return rule
        return None

    def upsert_rule(self, rule: dict):
        existing = self.find_rule(rule["exe"])
        if existing:
            existing.update(rule)
        else:
            self.rules.append(rule)
        self.save()

    def remove_rule(self, exe: str):
        self.active_profile["rules"] = [
            r for r in self.rules if r["exe"].lower() != exe.lower()
        ]
        self.save()

    # ---------- last language memory ----------
    def get_last_language(self, exe: str, fallback: str) -> str:
        return self.data["last_language"].get(exe.lower(), fallback)

    def set_last_language(self, exe: str, lang: str):
        self.data["last_language"][exe.lower()] = lang
        self.save()

    # ---------- stats ----------
    def bump_stat(self, exe: str):
        exe = exe.lower()
        self.data["stats"][exe] = self.data["stats"].get(exe, 0) + 1
        self.save()

    def get_stats(self) -> dict:
        return dict(self.data["stats"])

    # ---------- import / export ----------
    def export_to(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def import_from(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self.data = _deep_merge(DEFAULT_SETTINGS, loaded)
        self.save()

    # ---------- ریست کامل ----------
    def reset_to_defaults(self):
        """همه‌ی برنامه‌های اضافه‌شده، پروفایل‌ها، قوانین عنوان و آمار استفاده را
        پاک می‌کند و تنظیمات را به حالت اولیه (کارخانه‌ای) برمی‌گرداند."""
        self.data = copy.deepcopy(DEFAULT_SETTINGS)
        self.save()