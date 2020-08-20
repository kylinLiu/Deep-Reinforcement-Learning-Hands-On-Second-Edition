# coding: utf-8
"""
# @Time    : 2019/4/23 16:16
# @Author  : Kylin
# @File    : dbmodel.py
# @Software: PyCharm
# @Descript:
"""
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DbModel():
    def __init__(self,db_name):
        conn = sqlite3.connect('{}.db'.format(db_name), isolation_level=None)  # 自动提交
        conn.row_factory = dict_factory
        self.cursor = conn.cursor()
        sql = '''
            CREATE TABLE IF NOT EXISTS kzz_data(
            symbol CHAR(10) NOT NULL,
            ts int NOT NULL,
            data TEXT,
            d_type CHAR(10) NOT NULL
           );
        '''
        self.cursor.execute(sql)
        sql = '''
            CREATE UNIQUE INDEX IF NOT EXISTS kzz_data_unique ON kzz_data (symbol,ts,d_type);

        '''
        self.cursor.execute(sql)

    def fetchall(self, sql, *args):
        self.cursor.execute(sql, *args)
        return self.cursor.fetchall()

    def fetchone(self, sql, *args):
        self.cursor.execute(sql, *args)
        return self.cursor.fetchone()

    def execute(self, sql, *args):
        self.cursor.execute(sql, *args)
        return self.cursor.lastrowid

    def executemany(self, sql, *args):
        self.cursor.executemany(sql, *args)
        return self.cursor.lastrowid


if __name__ == "__main__":
    pass
