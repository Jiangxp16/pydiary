import atexit
import sqlite3

from core.util import utils

db_name = utils.load_config("global", "db_name")
conn = sqlite3.connect(db_name, check_same_thread=False)
cur = conn.cursor()


@atexit.register
def close_connection():
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(e.args)


def insert(sql_cmd, args=()):
    try:
        cur.execute(sql_cmd, args)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def insert_many(sql_cmd, args_list=[]):
    try:
        cur.executemany(sql_cmd, args_list)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def select_one(sql_cmd, args=()):
    try:
        cur.execute(sql_cmd, args)
        return cur.fetchone()
    except Exception as e:
        print(e.args)
        return None


def select(sql_cmd, args=()):
    try:
        cur.execute(sql_cmd, args)
        return cur.fetchall()
    except Exception as e:
        print(e.args)
        return []


def update(sql_cmd, args=()):
    try:
        cur.execute(sql_cmd, args)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def delete(sql_cmd, args=()):
    try:
        cur.execute(sql_cmd, args)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def get_last(table: str):
    rs = select_one("SELECT * FROM %s WHERE id=last_insert_rowid()" % table)
    return rs
