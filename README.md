<div align="center">

# AltoShift

**تغییر خودکار زبان کیبورد بر اساس برنامه‌ی فعال · Automatic keyboard language switching based on the active app**

![Platform](https://img.shields.io/badge/platform-Windows-6c5ce7?logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-TBD-lightgrey)

[🇮🇷 فارسی](#-فارسی) · [🇬🇧 English](#-english) · [⬇️ Download / دانلود](../../releases)

</div>

---

<a name="-فارسی"></a>

<div dir="rtl" align="right">

## 🇮🇷 فارسی

### معرفی

**AltoShift** یک ابزار ویندوزی است که زبان کیبورد را به‌صورت خودکار بر اساس برنامه‌ی فعال تغییر می‌دهد. دیگر لازم نیست هر بار بین برنامه‌ها جابه‌جا می‌شوید `Alt+Shift` بزنید. کافی است یک‌بار مشخص کنید هر برنامه با چه زبانی (فارسی یا انگلیسی) باز شود؛ AltoShift هر بار که روی آن برنامه بروید، زبان کیبورد را خودش تنظیم می‌کند.

تمام تنظیمات به‌صورت محلی روی سیستم شما ذخیره می‌شوند و برنامه برای کار کردن نیازی به اینترنت ندارد.

### ✨ امکانات

#### 🖥️ تشخیص و تغییر خودکار
- **تشخیص خودکار برنامه‌ی فعال** — نه فقط با کلیک، بلکه با `Alt+Tab`، کلیک روی تسک‌بار و هر روش دیگری هم کار می‌کند
- تعیین زبان برای هر برنامه: فارسی (FA)، انگلیسی (EN)، یا «به‌خاطر بسپار آخرین زبان»
- **قوانین پیشرفته بر اساس عنوان پنجره** — مثلاً در Chrome وقتی تب دیوار باز است زبان فارسی باشد و تب ChatGPT انگلیسی؛ هر برنامه می‌تواند چندین قانون مستقل داشته باشد
- **پروفایل‌های مجزا** (مثلاً «کار» و «برنامه‌نویسی») با مجموعه قوانین متفاوت، قابل جابه‌جایی سریع از منوی سینی سیستم

#### 🎛️ رابط کاربری و کنترل
- **آیکون سینی سیستم** با نمایش زنده‌ی زبان فعلی و منوی راست‌کلیک برای توقف موقت / پروفایل / خروج
- **میانبر سراسری** (قابل تنظیم، پیش‌فرض `Ctrl+Alt+K`) برای فعال/غیرفعال کردن سریع کل برنامه
- **نمایش کوتاه روی صفحه (OSD)** هر بار که زبان به‌صورت خودکار عوض شود
- **آیکون واقعی هر برنامه** (استخراج‌شده از فایل exe) با آواتار جایگزین در صورت نبودن آیکون
- **آمار استفاده** با نمودار میله‌ای — چندبار برای هر برنامه زبان خودکار تغییر کرده
- رابط کاربری **دوزبانه** (فارسی/انگلیسی) با تغییر زنده از تنظیمات
- تم **تیره و روشن**

#### ⚙️ امکانات سیستمی
- اجرای خودکار همراه ویندوز
- قفل تک‌نمونه‌ای (جلوگیری از اجرای همزمان چند نسخه)
- برون‌بری / درون‌ریزی تنظیمات برای پشتیبان‌گیری
- ریست کامل تنظیمات با یک کلیک

### 📦 نصب (برای کاربر نهایی)

1. به بخش **[Releases](../../releases)** بروید.
2. آخرین نسخه‌ی `AltoShift-Setup.exe` را دانلود کنید.
3. فایل را اجرا کنید. نصب‌کننده برنامه را داخل Program Files نصب می‌کند و میانبر دسکتاپ / منوی استارت می‌سازد.

> ⚠️ چون این exe امضای دیجیتال (Code Signing) ندارد، ممکن است ویندوز هشدار «ناشر ناشناس» (SmartScreen) بدهد؛ این طبیعی است.

### 🧰 تکنولوژی‌ها

| بخش | ابزار |
|:---|:---|
| زبان | Python 3.10+ |
| رابط کاربری | PySide6 (شامل QtCharts) |
| تعامل با سیستم | pywin32 + ctypes (Win32 API) |
| شناسایی پردازش‌ها | psutil |
| فونت فارسی | [Sahel](https://github.com/rastikerdar/sahel-font) |

### 📁 ساختار پروژه

```
AltoShift/
├── main.py                 # نقطه‌ی شروع و اتصال همه‌ی بخش‌ها
├── requirements.txt
├── assets/
│   ├── icon.png             # لوگوی برنامه (داخل اپ)
│   └── icon.ico             # آیکون فایل exe
├── fonts/                   # فونت‌های Sahel (باید دستی اضافه شوند)
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

### ⚙️ نکات فنی مهم

- برنامه‌هایی که با دسترسی **Administrator** اجرا می‌شوند (مثل Task Manager) فقط وقتی قابل‌کنترل‌اند که خود AltoShift هم با دسترسی Administrator اجرا شود.
- بعضی برنامه‌ها (مثل CMD، PowerShell، Git Bash) پنجره‌ی خودشان را ندارند و در واقع میزبانشان (`conhost.exe`، `WindowsTerminal.exe`، `mintty.exe`) صاحب پنجره است. برای این موارد از نشانگر زنده‌ی «پنجره‌ی فعال فعلی» استفاده کنید تا نام exe واقعی را پیدا کنید و در صورت نیاز از «قوانین عنوان» کمک بگیرید.
- چیدمان‌های زبان مقصد (مثل فارسی) باید از قبل در ویندوز نصب شده باشند (تنظیمات ویندوز ← زمان و زبان).

### 👨‍💻 توسعه‌دهنده

**امیرمحمد دهقانکار (A. DehghanKar)**

- 📧 ایمیل: amirdehghan438@gmail.com
- 🐙 گیت‌هاب: [AmirDehghanKar](https://github.com/AmirDehghanKar)

اگر پروژه برایتان مفید بود، با دادن ⭐ به مخزن از آن حمایت کنید.

</div>

---

<a name="-english"></a>

## 🇬🇧 English

### Introduction

**AltoShift** is a Windows utility that automatically switches the keyboard language based on the active application. You no longer need to press `Alt+Shift` every time you switch between apps. Just set once which language (Persian or English) each app should use, and AltoShift will handle the rest whenever you focus that application.

All settings are stored locally on your machine. No internet connection is required.

### ✨ Features

#### 🖥️ Automatic detection & switching
- **Automatic active-app detection** — works not only with mouse clicks, but also with `Alt+Tab`, taskbar clicks, and any other focus method
- Per-app language setting: Persian (FA), English (EN), or “Remember last language”
- **Advanced window-title rules** — e.g. in Chrome, use Persian for the Divar tab and English for the ChatGPT tab; each app can have multiple independent rules
- **Separate profiles** (e.g. “Work” and “Coding”) with different rule sets, switchable quickly from the system tray menu

#### 🎛️ UI & controls
- **System tray icon** with live current-language display and right-click menu for pause / profiles / exit
- **Global hotkey** (configurable, default `Ctrl+Alt+K`) to quickly enable/disable the whole app
- **On-screen display (OSD)** that briefly appears whenever the language is switched automatically
- **Real app icons** extracted from the executable, with a fallback avatar when no icon is available
- **Usage statistics** with bar charts — how many times the language was auto-switched per app
- **Bilingual UI** (Persian / English) with live switching from settings
- **Dark & light themes**

#### ⚙️ System features
- Start with Windows
- Single-instance lock (prevents multiple simultaneous runs)
- Export / import settings for backup
- One-click full settings reset

### 📦 Installation (end users)

1. Go to the **[Releases](../../releases)** page.
2. Download the latest `AltoShift-Setup.exe`.
3. Run the installer. It installs the app under Program Files and creates desktop / Start menu shortcuts.

> ⚠️ Because the executable is not code-signed, Windows may show an “Unknown publisher” (SmartScreen) warning. This is expected.

### 🧰 Tech stack

| Area | Tool |
|:---|:---|
| Language | Python 3.10+ |
| UI | PySide6 (including QtCharts) |
| System interaction | pywin32 + ctypes (Win32 API) |
| Process detection | psutil |
| Persian font | [Sahel](https://github.com/rastikerdar/sahel-font) |

### 📁 Project structure

```
AltoShift/
├── main.py                 # Entry point and wiring of all components
├── requirements.txt
├── assets/
│   ├── icon.png             # App logo (in-app)
│   └── icon.ico             # Executable icon
├── fonts/                   # Sahel fonts (must be added manually)
├── core/
│   ├── settings.py          # Save/load settings (JSON in %APPDATA%\AltoShift)
│   ├── language_utils.py    # Detect & change keyboard layout (Win32 API)
│   ├── window_monitor.py    # Listen for active window changes
│   ├── app_registry.py      # List of installed / running apps
│   ├── icon_utils.py        # Extract real icons from exe files
│   ├── hotkey.py            # Global hotkey registration
│   ├── startup.py           # Start with Windows
│   ├── single_instance.py   # Prevent multiple instances
│   ├── fonts.py             # Load Sahel fonts at runtime
│   └── engine.py            # Core decision engine & language switching
└── ui/
    ├── main_window.py       # Main window (Apps, Stats, Settings tabs)
    ├── add_app_dialog.py    # Add-app dialog
    ├── title_rules_dialog.py# Multi-rule dialog based on window title
    ├── tray.py               # System tray icon
    ├── osd.py                # Brief on-screen display
    ├── styles.py             # Dark/light QSS styles
    └── i18n.py               # UI translation system (Persian/English)
```

### ⚙️ Important technical notes

- Apps that run with **Administrator** privileges (e.g. Task Manager) can only be controlled if AltoShift itself is also running as Administrator.
- Some programs (CMD, PowerShell, Git Bash, etc.) do not own their own window; the host process (`conhost.exe`, `WindowsTerminal.exe`, `mintty.exe`) does. Use the live “current active window” indicator in the Apps tab to discover the real executable name, and use title rules when needed to distinguish multiple apps under the same host.
- Target language layouts (e.g. Persian) must already be installed in Windows (Settings → Time & Language).

### 👨‍💻 Developer

**Amirmohammad Dehghankar (A. DehghanKar)**

- 📧 Email: amirdehghan438@gmail.com
- 🐙 GitHub: [AmirDehghanKar](https://github.com/AmirDehghanKar)

If you find this project useful, consider giving the repo a ⭐.

---

<div align="center">

Made with Love❤️
</div>
```
