import mysql.connector

from constants import (
    DEFAULT_MYSQL_HOST,
    DEFAULT_MYSQL_PORT,
    DEFAULT_MYSQL_DB,
    DEFAULT_MYSQL_USER,
    DEFAULT_MYSQL_PASSKEY
)


class MysqlApi(object):
    def __init__(self, opts={}):
        self.host = opts.get('host') or DEFAULT_MYSQL_HOST
        self.port = opts.get('port') or DEFAULT_MYSQL_PORT
        self.db = opts.get('db') or DEFAULT_MYSQL_DB
        self.user = opts.get('user') or DEFAULT_MYSQL_USER
        self.passkey = opts.get('passkey') or DEFAULT_MYSQL_PASSKEY
        self.__connect()

    def __connect(self):
        self.conn = mysql.connector.connect(user=self.user, password=self.passkey, host=self.host, database=self.db,
                                              port=self.port)
        self.cursor = self.conn.cursor()

    def execute(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def get_records(self, query, params):
        self.cursor.execute(query, params)
        for record in self.cursor:
            yield record
