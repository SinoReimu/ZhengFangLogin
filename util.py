from StringIO import StringIO
import zlib
import gzip as gz
import urllib2

def read(response):
	encoding = response.info().get('Content-Encoding')
	content = response.read()
	if encoding == 'deflate':
		content = deflate(content)
	elif encoding == 'gzip':
		content = gzip(content)
	return content
	
def gzip(data):
	buf = StringIO(data)
	f = gz.GzipFile(fileobj=buf)
	return f.read()
	
def deflate(data):
	try:
		return zlib.decompress(data, -zlib.MAX_WBITS)
	except zlib.error:
		return zlib.decompress(data)
		
def getopener(cookie):
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	opener.addheaders = [('Cache-Control', 'max-age=0'),('Upgrade-Insecure-Requests','1'),('Origin', 'http://cas.hdu.edu.cn'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('Accept-Encoding','gzip, deflate, sdch'),('Accept-Language','zh-CN,zh;q=0.8'),('Host','jxgl.hdu.edu.cn'),('Referer','http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx'),('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36')]
	return opener
