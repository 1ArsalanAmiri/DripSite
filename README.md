This is a testing backend for the project "Drip" 
a persian clothing brand 
its getting completed 
now its just a product list and a accounting system


# DripSite

## راهنمای نصب و ران کردن پروژه با Docker Compose

این پروژه شامل **Backend Django* است. برای اجرای پروژه روی سیستم خود با Docker، مراحل زیر را دنبال کنید:

---

## 1. کلون کردن پروژه

```bash
git clone https://github.com/1ArsalanAmiri/DripSite.git
cd DripSite
2. اطمینان از نصب Docker
مطمئن شوید Docker روی سیستم شما نصب و در حال اجرا است.

Docker Compose معمولاً همراه Docker Desktop نصب می‌شود.

3. ساخت Docker Image ها
برای ساخت Image های پروژه (یک بار کافی است):

bash
Copy code
docker compose build
4. اجرای پروژه در پس‌زمینه
bash
Copy code
docker compose up -d
این دستور کانتینرهای Backend و Frontend را اجرا می‌کند.

5. بررسی وضعیت کانتینرها
bash
Copy code
docker compose ps
باید کانتینرهای پروژه در حال اجرا باشند.

6. مشاهده لاگ‌ها (اختیاری)
bash
Copy code
docker compose logs -f
7. خاموش کردن پروژه
bash
Copy code
docker compose down
این دستور کانتینرها را متوقف و حذف می‌کند.

⚡ نکات مهم
مرحله‌ی build فقط برای بار اول یا بعد از تغییرات Dockerfile یا فایل‌های اصلی پروژه ضروری است.

پروژه بدون نیاز به نصب مستقیم Python روی سیستم اجرا می‌شود.

برای تغییرات کد، کافیست فایل‌ها را ویرایش کرده و کانتینرها را ریستارت کنید.

🌐 دسترسی به پروژه
Backend: http://localhost:8000/
