<p align="center">
  <img src="https://raw.githubusercontent.com/OandONE/cron_shell/main/static/logo.png" width="120" alt="cron_shell">
</p>

<h1 align="center">⚡ CronShell</h1>
<p align="center"><strong>ترمینال مخفی برای هاست‌های اشتراکی — بدون نیاز به SSH</strong></p>

<p align="center">
  <a href="https://github.com/OandONE/cron_shell/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue" alt="Python 3.8-3.14"></a>
</p>

---

## 🤔 چرا CronShell؟

هاست‌های اشتراکی (cPanel) معمولاً دسترسی SSH رو می‌بندن.  
نه `pip` می‌تونی بزنی، نه `git`، نه حتی `ls -la`.

**CronShell** یه ترمینال واقعی بهت می‌ده — با قدرت cron و WebSocket.  
بدون SSH. بدون پورت باز. بدون دردسر.

---

## ✨ ویژگی‌ها

- 🔒 **بدون نیاز به SSH** — کاملاً با cron کار می‌کنه
- 🌐 **پنل تحت وب لحظه‌ای** — ترمینال با WebSocket
- 🎨 **تم دارک** — دقیقاً شبیه ترمینال لینوکس
- 📜 **تاریخچه دستورات** — Arrow Up/Down
- 🔑 **احراز هویت با توکن** — هیچ‌کس دیگه نمی‌تونه دسترسی داشته باشه
- 📁 **آرشیو لاگ‌ها** — خروجی هر دستور توی `logs/` ذخیره می‌شه
- 🛡️ **حالت امن** — blacklist/whitelist برای دستورات خطرناک
- 🪶 **سبک** — پایتون خالص، بدون دیتابیس
- 📦 **سازگار با cPanel** — نسخهٔ Flask + Socket.IO

---

## 📁 ساختار پروژه

```
cron_shell/
├── README.md
├── README_FA.md
│
└── cron_shell/
    ├── cronshell.py              # 🔧 موتور اصلی (اجرا توسط cron)
    ├── webpanel.py               # 🌐 پنل Flask + Socket.IO
    ├── webpanel_fastapi.py       # ⚡ پنل FastAPI + WebSocket
    ├── runner.sh                 # 🏃 نقطهٔ ورود cron
    ├── config.json               # ⚙️ تنظیمات
    ├── crontab                   # 📅 نمونه کرون‌جاب
    └── static/
        ├── panel.html            # 🖥️ رابط ترمینال (نسخهٔ Flask)
        ├── panel_fastapi.html    # 🖥️ رابط ترمینال (نسخهٔ FastAPI)
        └── vazir.woff2           # 🇮🇷 فونت فارسی وزیر
```

---

## 🐍 معرفی فایل‌های پایتون

### 1. `cronshell.py` — موتور اصلی

اسکریپت اصلی که cron هر دقیقه اجراش می‌کنه.

**چه کاری می‌کنه:**
- چک می‌کنه `command.sh` محتوا داره یا نه
- اگه داره: دستور رو اجرا می‌کنه، خروجی رو توی `logs/` ذخیره می‌کنه، `command.sh` رو خالی می‌کنه
- پشتیبانی از whitelist/blacklist برای امنیت
- پاکسازی خودکار لاگ‌های قدیمی

**کی استفاده کنی:** وقتی پنل تحت وب نمی‌خوای. فقط توی `command.sh` دستور بنویس.

```bash
echo "ls -la /home" > command.sh
# ۱ دقیقه صبر کن...
cat logs/result_*.log
```

---

### 2. `webpanel.py` — پنل Flask

ترمینال تحت وب با خروجی لحظه‌ای با **Flask + Socket.IO**.

**چه کاری می‌کنه:**
- یه صفحهٔ HTML به سبک ترمینال نشون می‌ده
- با WebSocket (Socket.IO) وصل می‌شه
- دستورات رو اجرا می‌کنه و خروجی رو لحظه‌ای نشون می‌ده
- احراز هویت با توکن
- همهٔ خروجی‌ها توی `logs/` ذخیره می‌شن

**کی استفاده کنی:** وقتی روی **cPanel یا هاست اشتراکی** هستی (ASGI کار نمی‌کنه).

**اجرا:**
```bash
pip install flask flask-socketio
python webpanel.py
# باز کن: http://your-server:9999/?token=YOUR_TOKEN
```

---

### 3. `webpanel_fastapi.py` — پنل FastAPI

همون پنل Flask، ولی با **FastAPI + WebSocket**.

**چه کاری می‌کنه:**
- همهٔ کارایی که `webpanel.py` می‌کنه
- پشتیبانی از async (عملکرد بهتر)
- WebSocket تمیزتر

**کی استفاده کنی:** وقتی روی **VPS یا سرور اختصاصی** هستی.

**اجرا:**
```bash
pip install fastapi uvicorn
python webpanel_fastapi.py
# باز کن: http://your-server:9999/?token=YOUR_TOKEN
```

---

## 📦 نصب

### ۱. آپلود روی هاست

پوشهٔ `cron_shell/` رو روی هاست آپلود کن.

### ۲. تنظیم cron job

محتویات فایل `crontab` رو توی **Cron Jobs** سی‌پنل وارد کن:

```bash
* * * * * /home/youruser/cron_shell/runner.sh
```

### ۳. تنظیم توکن

فایل `config.json` رو ویرایش کن:

```json
{
    "token": "یه-توکن-قوی-و-محرمانه",
    "sleep": 0,
    "timeout": 30,
    "log_retention": 7,
    "whitelist": [],
    "blacklist": ["rm -rf /", "mkfs", "dd if="]
}
```

### ۴. پنل رو اجرا کن

```bash
cd /home/youruser/cron_shell

# برای cPanel / هاست اشتراکی:
python webpanel.py

# برای VPS:
python webpanel_fastapi.py
```

### ۵. توی مرورگر باز کن

```
http://your-server-ip:9999/?token=یه-توکن-قوی-و-محرمانه
```

---

## 🔒 امنیت

- **توکن اجباری** — توی `config.json` تنظیم می‌شه
- **Blacklist** — دستورات خطرناک رو مسدود کن
- **Whitelist** — فقط دستورات خاص رو مجاز کن
- **بدون پورت باز** (برای حالت cron-only)

> ⚠️ فقط روی سرورهایی استفاده کن که مال خودت هستن یا اجازهٔ دسترسی داری.

---

## 📄 مجوز

MIT © [سید محمد حسین موسوی رجا (OandONE)](https://github.com/OandONE)

---

## 🤝 مشارکت

Pull Request خوشحالمون می‌کنه.  
باگ پیدا کردی؟ Issue باز کن.  
یه ویژگی جدید می‌خوای؟ Fork کن و بساز.
