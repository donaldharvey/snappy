import cookielib
from urllib import urlencode
import urllib2
import httplib
httplib.HTTPConnection.debuglevel = 1
import urlparse
from mimetypes import guess_type
from snappy.backend.httpstorage import WebStorage
from snappy.utils import MultipartDataHandler
from BeautifulSoup import BeautifulSoup
class TinyPicStorage(WebStorage):
	"""Uses TinyPic to store files online."""
	nice_name = 'TinyPic online storage'
	defaults = {
		'tinypic.email': '',
		'tinypic.password': '',
	}
	def __init__(self, configmanager):
		self.configmanager = configmanager

	def store(self, filepath):
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(1), urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		email = self.configmanager['tinypic.email']
		password = self.configmanager.get_password('tinypic.password')
		if email and password:
			data = urlencode({
				'action': 'login',
				'email': email,
				'password': password,
				'ref': '/'
			})
			opener.open('http://tinypic.com/login.php', data)
		tinypic_html = opener.open('http://tinypic.com').read()
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
		data['the_file'] = open(filepath)
		form_opener = urllib2.build_opener(urllib2.HTTPHandler(1), MultipartDataHandler, urllib2.HTTPCookieProcessor(cj))
		result = form_opener.open(upload_form['action'], data).read()
		return self._get_url_from_result(result)

	def _get_url_from_result(self, result):
		print result
		soup = BeautifulSoup(result)
		form = soup.find('form', {'name': 'myform'})
		try:
			pic_id = form.find('input', {'name': 'pic'})['value']
			server = form.find('input', {'name': 's'})['value']
		except TypeError:
			pic_id = form.find('input', {'name': 'upload[0][pic]'})['value']
			server = form.find('input', {'name': 'upload[0][s]'})['value']
		return 'http://s%s.tinypic.com/%s' % (server, pic_id)
