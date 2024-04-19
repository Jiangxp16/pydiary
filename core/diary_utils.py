import datetime
from typing import OrderedDict
from core import sqlutils, utils

sql_create = """
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    weather CHAR(50) NOT NULL,
    location CHAR(50) NOT NULL
);
"""
sqlutils.cur.execute(sql_create)


def add(date: datetime.date | int, content, weather='', location=''):
    if not content and not weather and not location:
        return
    _id = utils.date2int(date) if isinstance(date, datetime.date) else date
    return sqlutils.insert("INSERT INTO diary (id, content, weather, location) VALUES (?,?,?,?)",
                           (_id, content, weather, location))


def get_by_date(date: datetime.date | int):
    _id = utils.date2int(date) if isinstance(date, datetime.date) else date
    return sqlutils.select_one("SELECT id, content, weather, location FROM diary WHERE id=?", (_id,))


def get_between_dates(date1: datetime.date | int, date2: datetime.date | int):
    _id1 = utils.date2int(date1) if isinstance(date1, datetime.date) else date1
    _id2 = utils.date2int(date2) if isinstance(date2, datetime.date) else date2
    return sqlutils.select("SELECT id, content, weather, location FROM diary WHERE id BETWEEN ? AND ? ORDER BY id",
                           (_id1, _id2))


def get_month_diary(year, month):
    _id1 = year * 10000 + month * 100
    _id2 = _id1 + 31
    diaries = get_between_dates(_id1, _id2)
    return OrderedDict((diary[0], diary[1:4]) for diary in diaries)


def update(date: datetime.date | int, content, weather='', location=''):
    _id = utils.date2int(date) if isinstance(date, datetime.date) else date
    return sqlutils.update("UPDATE diary SET content=?, weather=?, location=? WHERE id=?",
                           (content, weather, location, _id))


def add_or_update(date: datetime.date | int, content, weather='', location=''):
    if get_by_date(date):
        return update(date, content, weather, location)
    return add(date, content, weather, location)


def delete(date: datetime.date | int):
    _id = utils.date2int(date) if isinstance(date, datetime.date) else date
    return sqlutils.delete("DELETE FROM diary where id=?", (_id,))


def update_diaries(diary_dict):
    res = True
    for _id in diary_dict:
        if not diary_dict[_id][0] and not diary_dict[_id][1] and not diary_dict[_id][2]:
            res &= delete(_id)
        else:
            res &= add_or_update(_id, diary_dict[_id][0], diary_dict[_id][1], diary_dict[_id][2])
    return res


def update_diary(date: datetime.date | int, diary: list):
    if not diary[0] and not diary[1] and not diary[2]:
        return delete(date)
    return add_or_update(date, diary[0], diary[1], diary[2])


def exp(file):
    diaries = get_between_dates(0, 99999999)
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(("Date", "Content", "Weather", "Location"))
    for diary in diaries:
        ws.append(list(diary))
    wb.save(file)


def imp(file):
    diary_dict = {}
    try:
        from openpyxl import load_workbook
        wb = load_workbook(file)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            diary = [cell.value for cell in row]
            diary_dict[diary[0]] = diary[1:4]
        return update_diaries(diary_dict)
    except Exception as e:
        print(e.args)
        return False
