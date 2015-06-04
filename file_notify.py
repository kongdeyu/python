#coding:utf-8


import logging
import os
import pyinotify

import config


g_log = logging.getLogger()


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, full_file_name):
        self.cf = config.Configure(full_file_name)

    def process_IN_DELETE(self, event):
        if not cmp(event.name, 'ds.conf'):
            g_log.warning('delete config file')

    def process_IN_MODIFY(self, event):
        if cmp(event.name, 'ds.conf'):
            return
        g_log.warning('modify config file, reload it')
        if not self.cf.load_conf():
            g_log.error('load config fail!')


def file_monitor(file_dir, file_name):
    wm = pyinotify.WatchManager() 
    mask = pyinotify.IN_DELETE | pyinotify.IN_MODIFY
    wm.add_watch(file_dir, mask, rec=True)
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler(os.path.join(file_dir, file_name)))
    g_log.info('start monitor config file')
    try:
        notifier.start()
    except:
        notifier.stop()


class Error(Exception):
    pass
