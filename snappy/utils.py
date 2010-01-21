import urllib2
import urllib
import os
from mimetools import choose_boundary
from mimetypes import guess_type
import stat
class Singleton(type):
	def __init__(self, name, bases, dict):
		super(Singleton, self).__init__(name, bases, dict)
		self.instance = None

	def __call__(self, *args, **kw):
		if self.instance is None:
			self.instance = super(Singleton, self).__call__(*args, **kw)

		return self.instance

class MultipartDataHandler(urllib2.BaseHandler):
	"""
	A urllib2-based multipart/form-data poster, adapted slightly from
	http://odin.himinbi.org/MultipartPostHandler.py and
	http://code.activestate.com/recipes/146306/.
	"""
	handler_order = urllib2.HTTPHandler.handler_order - 20

	def http_request(self, request):
		data = request.get_data()
		if data is not None and data is not str:
			fields, files = [], []
			for key, value in data.items():
				if type(value) == file:
					files.append((key, value))
				else:
					fields.append((key, value))
			if not len(files):
				# no files, so go straight ahead and encode the data
				data = urllib.urlencode(fields, True)
			else:
				content_type, data = self._encode_multipart_formdata(fields, files)
				req_content_type = request.get_header('Content-Type', '')
				if 'multipart/form-data' in req_content_type:
					request.set_header('Content-Type', content_type)
				else:
					request.add_unredirected_header('Content-Type', content_type)
			request.add_data(data)
		return request

	https_request = http_request

	def _encode_multipart_formdata(self, fields, files):
		"""
		fields is a sequence of (name, value) elements for regular form fields.
		files is a sequence of (name, filename, value) elements for data to be uploaded as files
		Return (content_type, body) ready for httplib.HTTP instance
		"""
		boundary = choose_boundary()
		CRLF = '\r\n'
		L = []
		for (key, value) in fields:
			L.append('--' + boundary)
			L.append('Content-Disposition: form-data; name="%s"' % str(key))
			L.append('')
			L.append(str(value))
		for (key, fd) in files:
			L.append('--' + boundary)
			filename = os.path.basename(fd.name)
			filesize = os.fstat(fd.fileno())[stat.ST_SIZE]
			L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(os.path.basename)))
			mimetype = guess_type(filename)[0] or 'application/octet-stream'
			L.append('Content-Type: %s' % mimetype)
			L.append('Content-Length: %s' % filesize)
			L.append('')
			fd.seek(0)
			L.append(fd.read())
		L.append('--' + boundary + '--')
		L.append('')
		body = CRLF.join(L)
		contenttype = 'multipart/form-data; boundary=%s' % boundary
		return contenttype, body
