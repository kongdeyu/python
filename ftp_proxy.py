#coding:utf-8


import ftplib
import os


class FTPProxy(object):

    def __init__(
            self,
            ip,
            port,
            user,
            passwd,
            backup_dir):
        self.conn = ftplib.FTP()
        self.back_dir = backup_dir
        try:
            self.conn.connect(host=ip, port=port)
            self.conn.login(user=user, passwd=passwd)
            self.conn.cwd(self.back_dir)
        except Exception as e:
            #self.conn.quit()
            raise Error(e)

    def close(self):
        try:
            self.conn.quit()
        except Exception as e:
            raise Error(e)

    def cd2dir(self, subdirlist):
        back_dir = self.back_dir
        for item in subdirlist:
            back_dir = os.path.join(back_dir, item)
            try:
                self.conn.cwd(back_dir)
            except Exception as e:
                self.conn.mkd(back_dir)
        self.conn.cwd(back_dir)

    def upload(self, filedir, filename):
        try:
            with open(os.path.join(filedir, filename), 'rb') as f:
                self.conn.storbinary('stor ' + filename, f)
        except Exception as e:
            raise Error(e)


class Error(Exception):
    pass
