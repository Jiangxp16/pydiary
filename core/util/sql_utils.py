import atexit
import sqlite3

from core.util import encrypt_utils, utils

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


def execute(sql_cmd, args=(), encrypt=True):
    try:
        if encrypt:
            args = encrypt_utils.encrypt(args)
        cur.execute(sql_cmd, args)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def execute_many(sql_cmd, args_list=[], encrypt=True):
    try:
        if encrypt:
            args_list = encrypt_utils.encrypt(args_list)
        cur.executemany(sql_cmd, args_list)
        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        return False
    return True


def select_one(sql_cmd, args=(), decrypt=True):
    try:
        cur.execute(sql_cmd, args)
        rs = cur.fetchone()
        if rs and decrypt:
            rs = encrypt_utils.decrypt(rs)
        return rs
    except Exception as e:
        print(e.args)
        return None


def select(sql_cmd, args=(), decrypt=True):
    try:
        cur.execute(sql_cmd, args)
        rs_list = cur.fetchall()
        if decrypt:
            rs_list = encrypt_utils.decrypt(rs_list)
        return rs_list
    except Exception as e:
        print(e.args)
        return []


def get_last(table: str, decrypt=True):
    rs = select_one("SELECT * FROM %s WHERE id=last_insert_rowid()" % table)
    if decrypt:
        rs = encrypt_utils.decrypt(rs)
    return rs
