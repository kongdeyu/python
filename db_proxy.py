#coding:utf-8


import contextlib
import logging
import MySQLdb


g_log = logging.getLogger()


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
            g_log.warn('error:%s' % (e))
            raise Error(e)

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            g_log.warn('error:%s' % (e))
            raise Error(e)

    @staticmethod
    def escape_string(cnt):
        try:
            return MySQLdb.escape_string(cnt)
        except Exception as e:
            g_log.warn('error:%s' % (e))
            raise Error(e)

    # private attribute
    def __commit(self):
        self.conn.commit()

    def __rollback(self):
        self.conn.rollback()

    def execute(self, sql, is_commit=True):
        try:
            self.conn.ping()
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(sql)
                if is_commit:
                    self.__commit()
        except Exception as e:
            g_log.warn('error:%s, rollback' % (e))
            self.__rollback()
            raise Error(e)

    def insert(self, sql, is_commit=True):
        self.execute(sql, is_commit)

    def delete(self, sql, is_commit=True):
        self.execute(sql, is_commit)

    def fetch_list(self, sql):
        try:
            self.conn.ping()
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            g_log.warn('error:%s' % (e))
            raise Error(e)

    def fetch_dict(self, sql):
        try:
            self.conn.ping()
            with contextlib.closing(
                    self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)) as cursor:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            g_log.warn('error:%s' % (e))
            raise Error(e)


class Error(Exception):
    pass
