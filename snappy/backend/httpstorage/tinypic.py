import urllib
import httplib
import urlparse
from mimetypes import guess_type
from snappy.backend.httpstorage import WebStorage, post_multipart
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
		result = post_multipart(
			upload_form['action'],
			data.items(),
			[('the_file', filepath, value)]
		).read()
		return self._get_url_from_result(result)

	def _get_url_from_result(self, result):
		soup = BeautifulSoup(result)
		form = soup.find('form', {'name': 'myform'})
		pic_id = form.find('input', {'name': 'pic'})['value']
		server = form.find('input', {'name': 's'})['value']
		return 'http://s%s.tinypic.com/%s' % (server, pic_id)
