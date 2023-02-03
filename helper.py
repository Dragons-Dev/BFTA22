import sqlite3
from pathlib import Path
import os


PATH = Path("./db/main.sqlite")


def yeet():
    with sqlite3.connect(PATH) as db:
        db.execute("DROP TABLE hausaufgaben")
        db.commit()


yeet()
