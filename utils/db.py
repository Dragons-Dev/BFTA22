import datetime
from pathlib import Path
import os

import aiosqlite
PATH = Path("./db/main.sqlite")


async def setup():
    if not PATH.exists():
        open(PATH, "w").close()
    async with aiosqlite.connect(PATH) as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS hausaufgaben (id INTEGER PRIMARY KEY AUTOINCREMENT, fach TEXT, aufgabe TEXT, wann TEXT)")
        await db.commit()


async def insert_hausaufgaben(fach: str, aufgabe: str, wann: datetime.date):
    async with aiosqlite.connect(PATH) as db:
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO hausaufgaben (fach, aufgabe, wann) VALUES (?, ?, ?)",
                                 (fach, aufgabe, wann.strftime("%Y-%m-%d")))
        await db.commit()


async def delete_hausaufgaben(id: int):
    async with aiosqlite.connect(PATH) as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM hausaufgaben WHERE id = ?", (id,))
        await db.commit()


async def get_hausaufgaben():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days = 1)
    after_tomorrow = today + datetime.timedelta(days = 2)
    print(tomorrow, after_tomorrow)
    async with aiosqlite.connect(PATH) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT id, fach, aufgabe, wann FROM hausaufgaben WHERE wann=? OR wann=?",
                                 (tomorrow, after_tomorrow))
            fetched_entries = await cursor.fetchall()
            if fetched_entries is None:
                return None
            else:
                return fetched_entries
