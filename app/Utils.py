from enum import Enum, auto
import sqlite3


class DbAction(Enum):
    fetchone = auto()
    fetchall = auto()
    commit = auto()
    none = auto()


def execute_action(query, args, action):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = None
    if action == DbAction.fetchone:
        result = cursor.fetchone()
    elif action == DbAction.fetchall:
        result = cursor.fetchall()
    elif action == DbAction.commit:
        conn.commit()
        result = cursor.lastrowid
    cursor.close()
    conn.close()
    return result