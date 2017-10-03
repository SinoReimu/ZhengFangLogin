from StringIO import StringIO
import zlib
import gzip as gz

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
		
