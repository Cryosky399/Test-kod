import asyncpg
from app.config import DB_URL

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=DB_URL)
    return _pool

async def get_animes():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM animelar ORDER BY id DESC")
        return [dict(row) for row in rows]

async def add_anime(nom, rams, qismi, davlat, tili, yili, janri):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO animelar (nom, rams, qismi, davlat, tili, yili, janri, qidiruv, sana, aniType) 
               VALUES ($1, $2, $3, $4, $5, $6, $7, 0, '', '')""",
            nom, rams, qismi, davlat, tili, yili, janri
        )

async def get_users():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM user_id")
        return [dict(row) for row in rows]

async def add_user(user_id, status, sana):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO user_id (user_id, status, sana) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO NOTHING",
            str(user_id), status, sana
        )

async def get_user_profile(user_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM user_id WHERE user_id = $1", str(user_id))
        return dict(row) if row else None

async def ban_user(user_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE user_id SET status='ban' WHERE user_id=$1", str(user_id))

async def unban_user(user_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE user_id SET status='active' WHERE user_id=$1", str(user_id))

async def get_stats():
    pool = await get_pool()
    async with pool.acquire() as conn:
        users = await conn.fetchval("SELECT COUNT(*) FROM user_id")
        animes = await conn.fetchval("SELECT COUNT(*) FROM animelar")
        return users, animes
