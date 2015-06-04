#coding:utf-8


import MySQLdb


class DBProxy(object):

    def __init__(
            self,
            host,
            port,
            user,
            passwd,
            db,
            charset='utf-8'):
        try:
            self.conn = MySQLdb.connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                db=db,
                charset=charset)
        except Exception as e:
            raise Error(e)

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            raise Error(e)

    @staticmethod
    def escape_string(cnt):
        try:
            return MySQLdb.escape_string(cnt)
        except Exception as e:
            raise Error(e)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def execute(self, sql, is_commit=True):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            if is_commit:
                self.commit()
        except Exception as e:
            self.rollback()
            raise Error(e)
        finally:
            cursor.close()

    def insert(self, sql, is_commit=True):
        self.execute(sql, is_commit)

    def delete(self, sql, is_commit=True):
        self.execute(sql, is_commit)

    def fetch_list(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise Error(e)
        finally:
            cursor.close()

    def fetch_dict(self, sql):
        try:
            cursor = self.conn.cursor(
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise Error(e)
        finally:
            cursor.close()


class Error(Exception):
    pass
