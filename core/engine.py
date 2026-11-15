"""
موتور اصلی تغییر زبان (core/engine.py)

وقتی پنجره‌ی فعال سیستم تغییر کند:
  ۱) بررسی می‌کند آیا برنامه فعال است (ماستر سوییچ روشن است؟)
  ۲) قانون مربوط به این exe را پیدا می‌کند؛ اگر برنامه در لیست تعریف نشده
     باشد، هیچ کاری انجام نمی‌شود (زبان کیبوردش دست‌نخورده می‌ماند)
  ۳) اگر قانون بر اساس عنوان پنجره داشت، آن را اعمال می‌کند؛ وگرنه زبان پیش‌فرض رویه
  ۴) اگر حالت REMEMBER بود، آخرین زبان استفاده‌شده برای آن برنامه را می‌خواند
  ۵) با کمی تأخیر (QTimer، نه sleep، تا UI فریز نشود) زبان را اعمال می‌کند؛
     این تأخیر لازم است چون بلافاصله بعد از تغییر پنجره‌ی فعال، ویندوز هنوز
     وضعیت واقعی کیبورد آن پنجره را به‌روز نکرده و خواندن زودهنگامش می‌تواند
     غلط باشد (همان باگِ «گاهی جواب می‌دهد، گاهی نه»)
  ۶) آمار را به‌روز می‌کند و OSD/Tray را مطلع می‌کند
"""

from PySide6.QtCore import QTimer

from core import language_utils
from core.window_monitor import ForegroundWindowMonitor


class SwitcherEngine:
    def __init__(self, settings, on_language_switched=None, on_window_focused=None):
        self.settings = settings
        self.on_language_switched = on_language_switched  # callback(lang_key)
        # callback(exe, title) — برای هر پنجره‌ی فعال صدا زده می‌شه (حتی اگه قانونی
        # براش نباشه)، تا بشه توی رابط کاربری اسم واقعی exe رو برای تشخیص دید
        # (مثلاً فهمیدن اینکه CMD/PowerShell واقعاً به اسم conhost.exe شناخته می‌شن)
        self.on_window_focused = on_window_focused
        self._rules_by_exe = {}
        self._pending_timers = []  # رفرنس موقت تا تایمرها قبل از اجرا GC نشوند
        self.reload_rules()
        self.monitor = ForegroundWindowMonitor(self._on_foreground_changed)

    def reload_rules(self):
        self._rules_by_exe = {r["exe"].lower(): r for r in self.settings.rules}

    def start(self):
        return self.monitor.start()

    def stop(self):
        self.monitor.stop()

    def _resolve_lang_for(self, rule: dict, title: str) -> str:
        for title_rule in rule.get("title_rules", []):
            if title_rule["contains"].lower() in title.lower():
                return title_rule["lang"]

        lang = rule.get("lang", "EN")
        if lang == "REMEMBER":
            return self.settings.get_last_language(rule["exe"], fallback="EN")
        return lang

    def _on_foreground_changed(self, exe: str, title: str, hwnd):
        if not exe:
            return

        # همیشه (حتی وقتی قانونی تعریف نشده یا ماستر سوییچ خاموشه) خبر بده تا
        # رابط کاربری بتونه اسم واقعی exe پنجره‌ی فعال رو نشون بده
        if self.on_window_focused:
            self.on_window_focused(exe, title)

        if not self.settings.general.get("enabled", True):
            return

        exe_key = exe.lower()
        rule = self._rules_by_exe.get(exe_key)
        if not rule:
            return

        target_lang = self._resolve_lang_for(rule, title)

        # حداقل ۵۰ میلی‌ثانیه تأخیر (قابل تنظیم از تب تنظیمات) تا ویندوز
        # فرصت کند وضعیت کیبورد پنجره‌ی تازه‌فعال‌شده را به‌روز کند
        delay_ms = max(int(self.settings.general.get("switch_delay_ms", 50)), 40)

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._apply_switch(hwnd, rule, target_lang, timer))
        timer.start(delay_ms)
        self._pending_timers.append(timer)

    def _apply_switch(self, hwnd, rule: dict, target_lang: str, timer: QTimer):
        if timer in self._pending_timers:
            self._pending_timers.remove(timer)

        # اگر در همین فاصله‌ی کوتاه، کاربر به پنجره‌ی دیگری رفته باشد،
        # این سوییچِ قدیمی را روی پنجره‌ی اشتباه اعمال نکن
        if language_utils.get_foreground_window() != hwnd:
            return

        # حالا که کمی زمان گذشته، خواندن زبان فعلی قابل‌اعتمادتر است
        current_lang = language_utils.current_language_key(hwnd)

        # آمار و «آخرین زبان» همیشه وقتی قانون اعمال می‌شه ثبت می‌شن، چه نیاز به
        # تغییر واقعی API باشه چه نه — چون ویندوز خودش گاهی زبان رو از قبل برای
        # همون پنجره به‌خاطر داره و تغییر واقعی لازم نیست، ولی از نظر کاربر این
        # «استفاده» از قانون محسوب می‌شه و باید توی آمار دیده بشه
        self.settings.set_last_language(rule["exe"], target_lang)
        self.settings.bump_stat(rule["exe"])

        if current_lang == target_lang:
            return  # از قبل درست بوده؛ نیازی به فراخوانی API و نمایش OSD نیست

        ok = language_utils.set_window_language(hwnd, target_lang)
        if ok and self.on_language_switched:
            self.on_language_switched(target_lang)