#coding:utf8


import contextlib
import logging
import os
import re
import time
import urllib2


ACCESS_TYPE = 0
PATTERN = re.compile('(?<=< HTTP/\d.\d )\d+(?= \w+)', re.S)
HEADERS = {'User-Agent'
        :'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

log = logging.getLogger()


def request_interface(t):
    if t == 0:
        def request(fun):
            def __decorator(url):
                cmd = '\'%s\'' % (url)
                resp = os.popen3('curl -g ' + cmd + ' -v')
                try:
                    code = None
                    info = resp[2].read()
                    resp[2].close()
                    res = resp[1].read().strip('\r\n')
                    resp[1].close()
                    for m in PATTERN.finditer(info):
                        code = int(m.group())
                    log.info('url:%s, http status code:%d' % (url, code))
                    if code != 200:
                        return
                    return res
                except:
                    log.info('url:%s, error' % (url))
            return __decorator
        return request
    else:
        def request(fun):
            def __decorator(url):
                try:
                    res = None
                    req = urllib2.Request(url, headers=HEADERS)
                    with contextlib.closing(urllib2.urlopen(req)) as resp:
                        res = resp.read().strip('\r\n')
                    return res
                except urllib2.URLError as e:
                    log.info('url:%s, error:%s, http fail' % (url, e))
                except:
                    log.info('url:%s, error' % (url))
            return __decorator
        return request


@request_interface(t=ACCESS_TYPE)
def request_response(url):
    pass


class Error(Exception):
    pass
