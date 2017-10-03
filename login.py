#!/usr/bin/python
import urllib2
import cookielib
import zlib
import hashlib
import sys
import os
import urllib
import re
from util import read

# get arguments

if len(sys.argv) < 3:
	print('usage:python login.py [username] [password]')
	sys.exit(0)
else:
	username = sys.argv[1]
	password = sys.argv[2]

# init my opener

cookie = cookielib.MozillaCookieJar('cookie.dat')
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
opener.addheaders = [('Cache-Control', 'max-age=0'),('Upgrade-Insecure-Requests','1'),('Origin', 'http://cas.hdu.edu.cn'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('Accept-Encoding','gzip, deflate, sdch'),('Accept-Language','zh-CN,zh;q=0.8'),('Host','jxgl.hdu.edu.cn'),('Referer','http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx'),('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36')]

# cas get ticket

para_dct = {}

para_dct['serviceName'] = 'null'
para_dct['LoginErrCnt'] = '0'
para_dct['username'] = username
para_dct['password'] = hashlib.md5(password).hexdigest()
para_dct['lt'] = re.compile('name="lt" value="(.*)"').search(read(response)).groups()[0]
para_dct['encodedService'] = 'http%3A%2F%2Fjxgl.hdu.edu.cn%2Fdefault.aspx'
para_dct['service'] = 'http://jxgl.hdu.edu.cn/default.aspx'
para_data = urllib.urlencode(para_dct)
resp2 = opener.open('http://cas.hdu.edu.cn/cas/login', para_data)

# redict to get cookies

url = re.compile('window.location.href="(.*)"').search(read(opener.open('http://jxgl.hdu.edu.cn'))).groups()[0]
opener.addheaders = [('Referer', 'http://cas.hdu.edu.cn/cas/login')]
url = re.compile('window.location.href="(.*)"').search(read(opener.open(url))).groups()[0]
url = re.compile("location.href='(.*)'").search(read(opener.open(url))).groups()[0]
url = re.compile('window.location.href="(.*)"').search(read(opener.open(url))).groups()[0]
opener.open(url)

# save the cookie

cookie.save(ignore_discard=True, ignore_expires=True)
