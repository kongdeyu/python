#coding:utf-8


import ConfigParser
import os
import threading


class Configure(object):
    conf = {}

    def __init__(self, full_file_name):
        self.lock = threading.Lock()
        self.full_file_name = full_file_name

    def __getitem__(self, section):
        with self.lock:
            option = None
            if section in Configure.conf:
                option = Configure.conf[section]

        return option

    # private attribute
    def __get_item(self, section, option):
        try:
            return self.cf.get(section, option)
        except Exception as e:
            print 'error:%s, get item fail!' % (e)
            raise Error(e)

    def __get_item_int(self, section, option):
        try:
            return self.cf.getint(section, option)
        except Exception as e:
            print 'error:%s, get item fail!' % (e)
            raise Error(e)

    def load_conf(self):
        if not os.path.exists(self.full_file_name):
            print 'no config file!'
            return False

        with self.lock:
            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.full_file_name)

            try:
                Configure.conf['dbhost'] = self.__get_item('db', 'host')
                Configure.conf['dbport'] = self.__get_item_int('db', 'port')
                return True
            except Exception as e:
                print 'error:%s, load conf fail!' % (e)
                return False


class Error(Exception):
    pass
