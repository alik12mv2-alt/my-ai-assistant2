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

## ذخیرهٔ تاریخچه
به‌صورت پیش‌فرض ذخیرهٔ تاریخچه خاموش است. برای فعال‌کردن ذخیرهٔ محلی گفتگوها، در `.env` مقدار `SAVE_HISTORY=true` قرار دهید. این کار یک فایل `chat_history.json` روی دستگاه ایجاد می‌کند؛ فایل را با دیگران به اشتراک نگذارید. برای حذف گفتگو از فرمان `reset` استفاده کنید.

## فرمان‌ها
- `help`: راهنما
- `reset`: پاک کردن تاریخچهٔ گفت‌وگو
- `exit`: خروج


---

## پروژه زرین آرمان (نسخه نمایشی)

- [باز کردن سایت](https://alik12mv2-alt.github.io/zarrin-arman2/)
- [پنل مدیریت کاتالوگ](https://alik12mv2-alt.github.io/zarrin-arman2/admin.html)
- [پوشه سورس سایت](./zarrin-arman/)
- [راهنمای راه‌اندازی](./zarrin-arman/README-SETUP.md)

> سایت فعلاً صرفاً نمایش نمونه است؛ قیمت‌ها نمونه‌اند و پرداخت/سفارش واقعی فعال نیست.
