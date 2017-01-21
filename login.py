#!/usr/bin/python
import urllib2
import cookielib
import zlib
import hashlib
import os
import urllib
import re
    
cookie = cookielib.MozillaCookieJar('cookie.dat')
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
opener.addheaders = [('Cache-Control', 'max-age=0'),('Upgrade-Insecure-Requests','1'),('Origin', 'http://cas.hdu.edu.cn'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('Accept-Encoding','gzip, deflate, sdch'),('Accept-Language','zh-CN,zh;q=0.8'),('Host','jxgl.hdu.edu.cn'),('Referer','http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx'),('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36')]
response = opener.open('http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx')
with open("Captcha.jpg", "wb") as code:
    code.write(opener.open("http://cas.hdu.edu.cn/cas/Captcha.jpg").read())
username = raw_input('input number:')
password = raw_input('password:')
os.system("eog Captcha.jpg 1>/dev/null 2>&1 &")
para_dct = {}
para_dct['serviceName'] = 'null'
para_dct['LoginErrCnt'] = '0'
para_dct['username'] = username
para_dct['password'] = hashlib.md5(password).hexdigest()
para_dct['lt'] = re.compile('name="lt" value="(.*)"').search(response.read()).groups()[0]
para_dct['encodedService'] = 'http%3A%2F%2Fjxgl.hdu.edu.cn%2Fdefault.aspx'
para_dct['service'] = 'http://jxgl.hdu.edu.cn/default.aspx'
para_dct['captcha'] = raw_input('input the captcha:')
para_data = urllib.urlencode(para_dct)
resp2 = opener.open('http://cas.hdu.edu.cn/cas/login', para_data)
url = re.compile('window.location.href="(.*)"').search(opener.open('http://jxgl.hdu.edu.cn').read()).groups()[0]
opener.addheaders = [('Referer', 'http://cas.hdu.edu.cn/cas/login')]
url = re.compile('window.location.href="(.*)"').search(opener.open(url).read()).groups()[0]
url = re.compile("location.href='(.*)'").search(opener.open(url).read()).groups()[0]
url = re.compile('window.location.href="(.*)"').search(opener.open(url).read()).groups()[0]
opener.open(url)
opener.open('http://jxgl.hdu.edu.cn/xs_main.aspx?xh='+username)
cookie.save(ignore_discard=True, ignore_expires=True)
