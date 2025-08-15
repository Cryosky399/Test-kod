import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from app.db import (
    get_animes, add_anime, get_users, add_user, ban_user, unban_user, get_user_profile, get_stats
)
from app.config import BOT_TOKEN
import asyncio
from datetime import datetime

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

ADMINS = [5978950232]  # Admin user_id ro'yxati (o'zingizni qo'shing)

# Foydalanuvchi /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await add_user(message.from_user.id, "active", datetime.now().strftime("%Y-%m-%d"))
    await message.answer(
        "👋 Salom! Anime botiga xush kelibsiz.\n"
        "Yordam uchun /yordam ni bosing."
    )

# /yordam
@dp.message(Command("yordam"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>Bot komandalar ro'yxati:</b>\n\n"
        "👤 <b>Foydalanuvchi:</b>\n"
        "/animes - Anime ro'yxati\n"
        "/profil - Profilingiz\n"
        "\n"
        "🔑 <b>Admin:</b>\n"
        "/add_anime - Anime qo'shish\n"
        "/ban - Foydalanuvchini banlash\n"
        "/unban - Bandan chiqarish\n"
        "/foydalanuvchilar - Foydalanuvchilar ro'yxati\n"
        "/stat - Statistika"
    )

# /animes
@dp.message(Command("animes"))
async def cmd_animes(message: types.Message):
    animes = await get_animes()
    if not animes:
        await message.answer("Hozircha hech qanday anime yo'q.")
        return
    for anime in animes[:10]:
        matn = (
            f"<b>{anime['nom']}</b>\n"
            f"🎞 Qismlar: {anime['qismi']}\n"
            f"🌍 Davlat: {anime['davlat']}\n"
            f"🗣 Til: {anime['tili']}\n"
            f"📅 Yili: {anime['yili']}\n"
            f"🏷 Janr: {anime['janri']}"
        )
        # Fayl turi aniqlash (rasm/video)
        if anime['rams'].startswith('AgAC') or anime['rams'].startswith('CQAC'):
            await message.answer_photo(anime['rams'], caption=matn)
        elif anime['rams'].startswith('BAAC'):
            await message.answer_video(anime['rams'], caption=matn)
        else:
            await message.answer(matn)
    await message.answer("To'liq ro'yxatni saytimizdan ko'ring: https://yourrenderurl.com")

# /profil
@dp.message(Command("profil"))
async def cmd_profile(message: types.Message):
    profile = await get_user_profile(message.from_user.id)
    if not profile:
        await message.answer("Profil topilmadi.")
        return
    await message.answer(
        f"🆔 ID: <code>{profile['user_id']}</code>\n"
        f"📅 Ro'yxatdan o'tgan sana: {profile['sana']}\n"
        f"🔖 Status: {profile['status']}"
    )

# ADMIN: /add_anime
@dp.message(Command("add_anime"))
async def cmd_add_anime(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    await message.answer(
        "Anime qo'shish uchun quyidagicha yuboring:\n"
        "<b>nom | rasm/video_file_id | qismlar | davlat | tili | yili | janr</b>\n\n"
        "Misol:\nNaruto | AgACAgUAAx... | 220 | Yaponiya | O'zbek | 2002 | Sarguzasht"
    )

@dp.message(F.text.regexp(r"^[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+$"))
async def handle_add_anime(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    try:
        nom, rams, qismi, davlat, tili, yili, janri = [s.strip() for s in message.text.split("|", 6)]
        await add_anime(nom, rams, qismi, davlat, tili, yili, janri)
        await message.answer("✅ Anime muvaffaqiyatli qo'shildi!")
    except Exception as e:
        await message.answer("❌ Xatolik! Ma'lumotlarni to'g'ri yuboring.")

# ADMIN: /ban
@dp.message(Command("ban"))
async def cmd_ban(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    await message.answer("Ban qilinadigan foydalanuvchi ID sini yuboring:")

@dp.message(F.text.regexp(r"^\d{6,}$"))
async def handle_ban(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    await ban_user(message.text.strip())
    await message.answer(f"{message.text.strip()} ban qilindi.")

# ADMIN: /unban
@dp.message(Command("unban"))
async def cmd_unban(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    await message.answer("Bandan chiqariladigan foydalanuvchi ID sini yuboring:")

@dp.message(F.text.regexp(r"^unban \d{6,}$"))
async def handle_unban(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    user_id = message.text.strip().replace("unban ", "")
    await unban_user(user_id)
    await message.answer(f"{user_id} bandan chiqarildi.")

# ADMIN: /foydalanuvchilar
@dp.message(Command("foydalanuvchilar"))
async def cmd_users(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    users = await get_users()
    text = "\n".join([f"{u['user_id']} - {u['status']}" for u in users])
    await message.answer(f"Foydalanuvchilar ro'yxati:\n\n{text[:4000]}")

# ADMIN: /stat
@dp.message(Command("stat"))
async def cmd_stat(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    users, animes = await get_stats()
    await message.answer(
        f"📊 Statistika:\n"
        f"👤 Foydalanuvchilar: {users}\n"
        f"🎬 Animes: {animes}"
    )
