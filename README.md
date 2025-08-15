# Anime Bot (O'zbekcha)

Ushbu loyiha Flask va aiogram asosida yozilgan anime Telegram bot va veb-sayt (faqat anime ro'yxati uchun).

## O'rnatish

1. Python 3.9+ va pip o'rnatilganligiga ishonch hosil qiling
2. `requirements.txt` orqali kutubxonalarni o'rnating:
    ```
    pip install -r requirements.txt
    ```
3. `.env` faylini quyidagicha yarating va to'ldiring:
    ```
    BOT_TOKEN=your_telegram_bot_token
    DB_URL=postgresql://user:pass@host:port/database
    ```
4. PostgreSQL bazangizda kerakli tablitsalarni yarating (strukturani eski MySQL dump asosida o'zgartiring).
5. Loyihani ishga tushiring:
    ```
    python main.py
    ```

## Komandalar

**Foydalanuvchi:**
- `/start` — Boshlash
- `/yordam` — Yordam va komandalar
- `/animes` — Anime ro'yxati
- `/profil` — Profilingiz

**Admin:**
- `/add_anime` — Anime qo'shish
- `/ban` — Foydalanuvchini ban qilish
- `/unban` — Ban ochish
- `/foydalanuvchilar` — Foydalanuvchilar ro'yxati
- `/stat` — Statistika

## Veb-sayt

- `http://localhost:5000` (yoki Render URL) — Anime ro'yxati

## Muallif

Cryosky399 uchun maxsus.
