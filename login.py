#!/usr/bin/python

import cookielib
import hashlib
import sys
import urllib
import re
from util import read, getopener

# get arguments

if len(sys.argv) < 3:
	print('usage:python login.py [username] [password]')
	sys.exit(0)
else:
	username = sys.argv[1]
	password = sys.argv[2]

# init my opener

cookie = cookielib.MozillaCookieJar('cookie.dat')
opener = getopener(cookie)

# cas get ticket

para_dct = {}
response = opener.open('http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx')

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
