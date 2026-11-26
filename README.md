# دستیار هوش مصنوعی شخصی

نسخهٔ اولیهٔ دستیار متنی فارسی برای اجرا در Termux.

## پیش‌نیازها
- Python
- API key از ارائه‌دهندهٔ API سازگار با Chat Completions

## راه‌اندازی در Termux
```bash
pkg update
pkg install python git
git clone https://github.com/alik12mv2-alt/my-ai-assistant2.git
cd my-ai-assistant2
cp .env.example .env
nano .env
python main.py
```

در فایل `.env` مقدار `API_KEY` را وارد کنید. کلید را در GitHub یا گفتگوها منتشر نکنید.

## فرمان‌های
- `help`: راهنما
- `reset`: پاک کردن تاریخچهٔ گفت‌وگوی همین اجرا
- `exit`: خروج

تاریخچه فقط در حافظهٔ موقت برنامه نگهداری می‌شود و به فایل ذخیره نمی‌شود. اطلاعات حساس وارد نکنید.
