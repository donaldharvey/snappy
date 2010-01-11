import urllib
import httplib
import urlparse
from mimetypes import guess_type
from snappy.backend.httpstorage import WebStorage
from BeautifulSoup import BeautifulSoup
class TinyPicStorage(WebStorage):
	"""Uses TinyPic to store files online."""
	nice_name = 'TinyPic online storage'
	defaults = {
		'tinypic.username': '',
		'tinypic.password': '',
	}
	def __init__(self, configmanager):
		self.configmanager = configmanager

	def store(self, filepath):
		tinypic_html = urllib.urlopen('http://tinypic.com').read()
		soup = BeautifulSoup(tinypic_html)
		upload_form = soup.find('form', {'id': 'uploadForm'})
		form_inputs = upload_form.findAll('input')
		data = {}
		for input in form_inputs:
			try:
				data[input['name']] = input['value']
			except KeyError:
				try:
					data[input['name']] = ''
				except KeyError:
					pass
		data['file_type'] = 'image'
		data['dimension'] = 1600
		f = open(filepath)
		try:
			value = f.read()
			print type(value)

		finally:
			f.close()
		result = self._post_multipart(
			upload_form['action'],
			data.items(),
			[('the_file', filepath, value)]
		)
		return self._get_url_from_result(result)

	# Following utility methods are slightly modified from http://code.activestate.com/recipes/146306/.
	@classmethod
	def _post_multipart(cls, url, fields, files):
		urlparts = urlparse.urlsplit(url)
		host, selector = urlparts[1], urlparts[2]
		"""
		Post fields and files to an http host as multipart/form-data.
		fields is a sequence of (name, value) elements for regular form fields.
		files is a sequence of (name, filename, value) elements for data to be uploaded as files
		Return the server's response page.
		"""
		content_type, body = cls._encode_multipart_formdata(fields, files)
		h = httplib.HTTP(host)
		h.putrequest('POST', selector)
		h.putheader('content-type', content_type)
		h.putheader('content-length', str(len(body)))
		h.endheaders()
		h.send(body)
		errcode, errmsg, headers = h.getreply()
		return h.file.read()

	@classmethod
	def _encode_multipart_formdata(cls, fields, files):
		"""
		fields is a sequence of (name, value) elements for regular form fields.
		files is a sequence of (name, filename, value) elements for data to be uploaded as files
		Return (content_type, body) ready for httplib.HTTP instance
		"""
		BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
		CRLF = '\r\n'
		L = []
		print fields
		for (key, value) in fields:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"' % str(key))
			L.append('')
			L.append(str(value))
		for (key, filename, value) in files:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(filename)))
			mimetype = guess_type(filename)[0] or 'application/octet-stream'
			L.append('Content-Type: %s' % mimetype)
			L.append('')
			L.append(str(value))
		L.append('--' + BOUNDARY + '--')
		L.append('')
		body = CRLF.join(L)
		content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
		return content_type, body

	def _get_url_from_result(self, result):
		soup = BeautifulSoup(result)
		form = soup.find('form', {'name': 'myform'})
		pic_id = form.find('input', {'name': 'pic'})['value']
		server = form.find('input', {'name': 's'})['value']
		return 'http://s%s.tinypic.com/%s' % (server, pic_id)

if __name__ == '__main__':
	from snappy.backend.configmanagers.fileconfigmanager import FileConfigManager
	configmanager = FileConfigManager()
	TinyPicStorage(configmanager).store('/home2/donald/fractal2.png')