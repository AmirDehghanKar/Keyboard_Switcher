# AltoShift

**تغییر خودکار زبان کیبورد بر اساس برنامه‌ی فعال، برای ویندوز.**

دیگه لازم نیست هر بار بین برنامه‌ها جابه‌جا می‌شی `Alt+Shift` بزنی. کافیه یک‌بار بگی هر برنامه با چه زبانی باز بشه (فارسی یا انگلیسی)، و AltoShift خودش هر بار که روی اون برنامه رفتی، زبان کیبورد رو خودکار تنظیم می‌کنه.

![platform](https://img.shields.io/badge/platform-Windows-6c5ce7)
![python](https://img.shields.io/badge/python-3.10%2B-6c5ce7)
![license](https://img.shields.io/badge/license-TBD-lightgrey)

---

## ✨ امکانات

- **تشخیص خودکار برنامه‌ی فعال** — نه فقط با کلیک، بلکه با `Alt+Tab`، کلیک روی تسک‌بار و هر روش دیگه‌ای هم کار می‌کنه.
- **تعیین زبان برای هر برنامه**: فارسی (FA)، انگلیسی (EN)، یا «به‌خاطر بسپار آخرین زبان».
- **قوانین پیشرفته بر اساس عنوان پنجره** — مثلاً توی Chrome، وقتی تب دیوار بازه زبان فارسی باشه ولی تب ChatGPT انگلیسی؛ هر برنامه می‌تونه چندین قانون مستقل داشته باشه.
- **پروفایل‌های مجزا** (مثلاً «کار» و «برنامه‌نویسی») با مجموعه قوانین متفاوت، قابل جابه‌جایی سریع از منوی سینی سیستم.
- **آیکون سینی سیستم** با نمایش زنده‌ی زبان فعلی، و منوی راست‌کلیک برای توقف موقت/پروفایل/خروج.
- **میانبر سراسری** (قابل تنظیم، پیش‌فرض `Ctrl+Alt+K`) برای فعال/غیرفعال کردن سریع کل برنامه.
- **نمایش کوتاه روی صفحه (OSD)** هر بار زبان خودکار عوض بشه.
- **آیکون واقعی هر برنامه** (استخراج‌شده از فایل exe)، با آواتار جایگزین در صورت نبودن آیکون.
- **آمار استفاده** با نمودار میله‌ای — چندبار برای هر برنامه زبان خودکار تغییر کرده.
- **رابط کاربری دوزبانه** (فارسی/انگلیسی) با تغییر زنده از تنظیمات.
- **تم تیره و روشن.**
- **اجرای خودکار همراه ویندوز**، قفل تک‌نمونه‌ای (جلوگیری از اجرای همزمان چند نسخه)، و برون‌بری/درون‌ریزی تنظیمات برای پشتیبان‌گیری.
- **ریست کامل** تنظیمات با یک کلیک (در صورت نیاز).

## 🖥️ تصاویر

> اسکرین‌شات‌های برنامه رو اینجا اضافه کن (پوشه‌ی `docs/screenshots/` پیشنهاد می‌شه).

## 📦 نصب (برای کاربر نهایی)

از بخش [Releases](../../releases) این ریپو، آخرین نسخه‌ی `AltoShift-Setup.exe` رو دانلود و اجرا کن. فایل نصب، برنامه رو داخل Program Files نصب می‌کنه و میانبر دسکتاپ/منوی استارت می‌سازه.

> ⚠️ چون این exe امضای دیجیتال (Code Signing) نداره، ممکنه ویندوز هشدار «ناشر ناشناس» (SmartScreen) بده؛ این طبیعیه.

## 🛠️ اجرا از روی سورس (برای توسعه)

نیازمندی‌ها: ویندوز ۱۰/۱۱، پایتون ۳.۱۰ یا بالاتر.

```powershell
git clone <repo-url>
cd AltoShift
py -m pip install -r requirements.txt
py main.py
```

### فونت

برنامه از فونت فارسی **Sahel** (نسخه‌های Light و Black) استفاده می‌کنه. فایل‌های `Sahel-Light.ttf` و `Sahel-Black.ttf` رو از [مخزن رسمی Sahel](https://github.com/rastikerdar/sahel-font/releases) دانلود کن و داخل پوشه‌ی `fonts/` بذار. اگه این فایل‌ها نباشن، برنامه با فونت پیش‌فرض ویندوز بدون کرش ادامه می‌ده.

## 📁 ساختار پروژه

```
AltoShift/
├── main.py                 # نقطه‌ی شروع و اتصال همه‌ی بخش‌ها
├── requirements.txt
├── assets/
│   ├── icon.png             # لوگوی برنامه (داخل اپ)
│   └── icon.ico             # آیکون فایل exe
├── fonts/                   # فونت‌های Sahel (باید دستی اضافه بشن)
├── core/
│   ├── settings.py          # ذخیره/بارگذاری تنظیمات (JSON در %APPDATA%\AltoShift)
│   ├── language_utils.py    # تشخیص و تغییر چیدمان کیبورد (Win32 API)
│   ├── window_monitor.py    # گوش دادن به تغییر پنجره‌ی فعال سیستم
│   ├── app_registry.py      # لیست برنامه‌های نصب‌شده / در حال اجرا
│   ├── icon_utils.py        # استخراج آیکون واقعی از فایل exe
│   ├── hotkey.py            # ثبت میانبر سراسری
│   ├── startup.py           # اجرای خودکار همراه ویندوز
│   ├── single_instance.py   # جلوگیری از اجرای همزمان چند نمونه
│   ├── fonts.py             # بارگذاری فونت‌های Sahel در زمان اجرا
│   └── engine.py            # موتور اصلی تصمیم‌گیری و تغییر زبان
└── ui/
    ├── main_window.py       # پنجره‌ی اصلی (تب برنامه‌ها، آمار، تنظیمات)
    ├── add_app_dialog.py    # دیالوگ افزودن برنامه
    ├── title_rules_dialog.py# دیالوگ قوانین متعدد بر اساس عنوان پنجره
    ├── tray.py               # آیکون سینی سیستم
    ├── osd.py                # نمایش کوتاه گوشه‌ی صفحه
    ├── styles.py             # استایل‌های تیره/روشن (QSS)
    └── i18n.py               # سیستم ترجمه‌ی رابط کاربری (فارسی/انگلیسی)
```

## 🚀 ساخت فایل exe و Installer

### ۱. نصب PyInstaller

```powershell
py -m pip install pyinstaller
```

### ۲. ساخت exe

```powershell
py -m PyInstaller --noconfirm --windowed --name "AltoShift" --icon "assets\icon.ico" --add-data "fonts;fonts" --add-data "assets;assets" --hidden-import "win32timezone" --hidden-import "win32com.client" main.py
```

خروجی اینجا ساخته می‌شه: `dist\AltoShift\AltoShift.exe`

### ۳. ساخت Installer (اختیاری، با Inno Setup)

[Inno Setup](https://jrsoftware.org/isdl.php) رو نصب کن، یه فایل `installer.iss` با تنظیمات `AppName=AltoShift` و `SetupIconFile=assets\icon.ico` بساز، و با `Ctrl+F9` کامپایلش کن. خروجی نهایی: `installer_output\AltoShift-Setup.exe`

## ⚙️ نکات فنی مهم

- برنامه‌هایی که با دسترسی **Administrator** اجرا می‌شن (مثل Task Manager) فقط وقتی قابل‌کنترل‌اند که خود AltoShift هم با دسترسی Administrator اجرا بشه.
- بعضی برنامه‌ها (مثل CMD، PowerShell، Git Bash) پنجره‌ی خودشون رو ندارن و در واقع میزبانشون (`conhost.exe`، `WindowsTerminal.exe`، `mintty.exe`) صاحب پنجره‌ست. برای این موارد، از نشانگر زنده‌ی «پنجره‌ی فعال فعلی» (توی تب برنامه‌ها) استفاده کن تا اسم exe واقعی رو پیدا کنی، و در صورت نیاز از «قوانین عنوان» برای تفکیک چند برنامه زیر یک میزبان مشترک کمک بگیر.
- چیدمان‌های زبان مقصد (مثل فارسی) باید از قبل در ویندوز نصب شده باشن (تنظیمات ویندوز ← زمان و زبان).

## 🧰 تکنولوژی‌ها

- [Python](https://python.org) 3.10+
- [PySide6](https://doc.qt.io/qtforpython/) (شامل QtCharts) برای رابط کاربری
- [pywin32](https://github.com/mhammond/pywin32) و `ctypes` برای تعامل با Win32 API
- [psutil](https://github.com/giampaolo/psutil) برای شناسایی پردازش‌ها
- فونت [Sahel](https://github.com/rastikerdar/sahel-font)

## 👤 طراح و برنامه‌نویس

**A.DehghanKar**
📧 amirdehghan438@gmail.com

## 📄 لایسنس

هنوز مشخص نشده — بعداً اضافه می‌شه.
