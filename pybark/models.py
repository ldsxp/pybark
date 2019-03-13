import os
import shortuuid
import sqlite3

# 创建 表
sql = """
CREATE TABLE 'devices' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'token' varchar(255) NOT NULL,
    'key' varchar(255) NOT NULL
)
"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database():
    def __init__(self, DB_PATH=None):

        if os.path.isfile(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS devices')
            c.execute(sql)
            conn.commit()

        conn.row_factory = dict_factory
        cur = conn.cursor()

        self.conn = conn
        self.cur = cur

    def get_token(self, key):
        """获取设备key对应的token"""

        # 查询
        rows = self.cur.execute('SELECT * FROM devices WHERE key=?', (key,)).fetchall()
        # print(rows)

        if rows:
            return rows[0]['token']

    def save_key(self, device_token, key):
        """保存token对应设备key"""

        # 查询
        rows = self.cur.execute('SELECT * FROM devices WHERE key=?', (key,)).fetchall()
        # print(rows, device_token, key)
        if len(rows) > 1:
            return False

        if rows:
            # 如果已经注册，则更新DeviceToken的值
            self.cur.execute('UPDATE `devices` SET token=? where key=?', (device_token, key))
        else:
            key = shortuuid.uuid()
            # 插入
            self.cur.execute('INSERT INTO `devices`(token, key) values (?,?)', (device_token, key))
        self.conn.commit()
        # print(key)
        return key
