# -*- coding: utf-8 -*-
"""
Работа с базой данных
"""
import csv
import sqlite3
# import contextlib
from PyQt5 import QtSql, QtCore

DB_PATH = "db/database.db"


# @contextlib.contextmanager
# def DataConn(db_name):
#     conn = sqlite3.connect(db_name)
#     yield # код из блока with выполнится тут
#     conn.close()


class DataConn:
    """
    Класс Context Manager
    Создает связь с базой данных SQLite и закрывает её по окончанию работы
    """

    def __init__(self, db_name):
        """Конструктор"""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Открываем подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.conn.close()
        if exc_val:
            raise


def create_table(table_name):
    """Создание базы данных"""
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            if table_name == 'table_8_4':
                # Создание таблицы "table_8_4"
                cursor.execute("""CREATE TABLE IF NOT EXISTS table_8_4
                                  (a_to_l INTEGER, n INTEGER, k_i_min REAL, k_i_max REAL)
                               """)
            elif table_name == 'table_8_5':
                # Создание таблицы "table_8_5"
                cursor.execute("""CREATE TABLE IF NOT EXISTS table_8_5
                                  (a_to_l INTEGER, n INTEGER, k_i_min REAL, k_i_max REAL)
                                  """)
            elif table_name == 'table_8_6':
                # Создание таблицы "table_8_6"
                cursor.execute("""CREATE TABLE IF NOT EXISTS table_8_6
                                  (a_to_l INTEGER, n INTEGER, k_i REAL)
                               """)
            elif table_name == 'table_8_7':
                # Создание таблицы "table_8_7"
                cursor.execute("""CREATE TABLE IF NOT EXISTS table_8_7
                                  (a_to_l INTEGER, n INTEGER, k_i REAL)
                               """)


# def set_data_to_table():
#     """Внесение данных в таблицу"""
#     with DataConn(DB_PATH) as conn:
#         with conn:
#             cursor = conn.cursor()
#
#             # # Внесение данных в таблицу "трансформатор"
#             # cursor.execute("""INSERT INTO transformer
#             #                   VALUES ('ГОСТ', 'ТМ', '10', '400', 'Y/Yн-0', '160', '2.7', '5.5')
#             #                   """)
#
#             # Внесение данных в таблицу "кабель"
#             cursor.execute("""INSERT INTO cable
#                               VALUES ('Кабель с алюминиевыми жилами в алюминиевой оболочке',
#                                       'Алюминий',
#                                       '4', '-1',
#                                       '9.61', '0.092', '10.95', '0.579')
#                               """)


def copy_from_csv_to_db(filename, tablename):
    """Копирование данных из файлов CSV в базу данных"""
    sql = {'table_8_4':
               ("""SELECT * FROM table_8_4 
                    WHERE a_to_l=? AND n=? AND k_i_min=? AND k_i_max=?""",
                'INSERT OR IGNORE INTO table_8_4 VALUES (?,?,?,?)'),
           'table_8_5':
               ("""SELECT * FROM table_8_4 
                    WHERE a_to_l=? AND n=? AND k_i_min=? AND k_i_max=?""",
                'INSERT OR IGNORE INTO table_8_5 VALUES (?,?,?,?)'),
           'table_8_6':
               ("""SELECT * FROM table_8_6
                    WHERE a_to_l=? AND n=? AND k_i=?""",
                'INSERT OR IGNORE INTO table_8_6 VALUES (?,?,?)'),
           'table_8_7':
               ("""SELECT * FROM table_8_7
                    WHERE a_to_l=? AND n=? AND k_i=?""",
                'INSERT OR IGNORE INTO table_8_7 VALUES (?,?,?)'),
           }
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            create_table(tablename)  # Создать таблицу, если не существует
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    cursor.execute(sql[tablename][0], row)
                    if not cursor.fetchall():  # проверка на существование идентичной записи
                        cursor.execute(sql[tablename][1], row)  # Внесение данных в таблицу


def find_tables():
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(DB_PATH)
    con.open()
    if con.isOpen():
        tables = con.tables()
    else:
        tables = []
        # s = "Возникла ошибка: " + con.lastError().text()
    con.close()
    # self.txtOutput.setText(s)

    # with DataConn(DB_PATH) as conn:
    #     cursor = conn.cursor()
    #     sql = "SELECT name FROM sqlite_temp_master WHERE type='table'"
    #     cursor.execute(sql)
    #     tables = [i[0] for i in cursor.fetchall()]
    return tables


def show_table(equipment):
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(DB_PATH)
    con.open()

    model = QtSql.QSqlQueryModel(parent=None)
    model.setQuery('select * from good order by goodname')
    # model.setSort(1, QtCore.Qt.AscendingOrder)
    # model.select()
    model.setHeaderData(1, QtCore.Qt.Horizontal, 'Завод изготовитель')
    model.setHeaderData(2, QtCore.Qt.Horizontal, 'Модель')
    model.setHeaderData(3, QtCore.Qt.Horizontal, 'Номинальное напряжение ВН')
    model.setHeaderData(4, QtCore.Qt.Horizontal, 'Номинальное напряжение НН')
    model.setHeaderData(5, QtCore.Qt.Horizontal, 'Схема соединения обмоток')
    model.setHeaderData(6, QtCore.Qt.Horizontal, 'Полная номинальная мощность')
    model.setHeaderData(7, QtCore.Qt.Horizontal, 'Потери короткого замыкания')
    model.setHeaderData(8, QtCore.Qt.Horizontal, 'Напряжение короткого замыкания')

    # equipment_table = con.record("transformer")
    # field_count = equipment_table.count()
    # for field in range(0, field_count):
    #     field_name = equipment_table.field(field).name()
    #     # if field_name != "id":
    #     #     self.cboSort.addItem(field_name)

    model.setQuery("select * from transformer")

    # stm = QtSql.QSqlRelationalTableModel()
    # stm.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    # stm.setTable(equipment)
    # # tables = con.tables()
    # # table_count = len(tables)
    # # if table_count > 0:
    # #     stm.
    # table = con.record(equipment)
    # field_count = table.count()
    # field_list = []
    # for field_index in range(0, field_count):
    #     field = table.field(field_index)
    #     field_list.append(field)
    #
    # stm.setSort(1, QtCore.Qt.AscendingOrder)
    # # stm.setRelation(3, QtSql.QSqlRelation('category', 'id', 'catname'))
    # stm.setRelation(3, QtSql.QSqlRelation(field_list))
    # stm.select()
    # stm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
    # stm.setHeaderData(2, QtCore.Qt.Horizontal, 'Кол-во')
    # stm.setHeaderData(3, QtCore.Qt.Horizontal, 'Категория')

    con.close()


def find_table_8_4(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT n, (k_i_min + k_i_max)/2 FROM table_8_4 WHERE a_to_l=?"
        cursor.execute(sql, args)
        result = [(i[0], i[1]) for i in cursor.fetchall()]
    result = list(zip(*result))
    # result = list(map(lambda x, y, z: (x, (y + z) / 2), *result))
    # result = list(zip(*result))
    return result


def find_table_8_5(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT n, (k_i_min + k_i_max)/2 FROM table_8_5 WHERE a_to_l=?"
        cursor.execute(sql, args)
        result = [(i[0], i[1]) for i in cursor.fetchall()]
    result = list(zip(*result))
    return result


def find_table_8_6(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT n, k_i FROM table_8_6 WHERE a_to_l=?"
        cursor.execute(sql, args)
        result = [(i[0], i[1]) for i in cursor.fetchall()]
    result = list(zip(*result))
    return result


def find_table_8_7(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT n, k_i FROM table_8_7 WHERE a_to_l=?"
        cursor.execute(sql, args)
        result = [(i[0], i[1]) for i in cursor.fetchall()]
    result = list(zip(*result))
    return result


if __name__ == "__main__":
    # copy_from_csv_to_db('db/Таблица_8-4.csv', 'table_8_4')
    # copy_from_csv_to_db('db/Таблица_8-5.csv', 'table_8_5')
    # copy_from_csv_to_db('db/Таблица_8-6.csv', 'table_8_6')
    # copy_from_csv_to_db('db/Таблица_8-7.csv', 'table_8_7')
    pass
