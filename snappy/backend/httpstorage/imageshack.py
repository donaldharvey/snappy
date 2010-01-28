import urllib2
from urllib import urlencode
import httplib
import urlparse
import os
import cookielib
from snappy.backend.httpstorage import WebStorage
from snappy.utils import MultipartDataHandler

class ImageShackStorage(WebStorage):
	"""Uses ImageShack to store files online."""
	nice_name = 'ImageShack online storage'
	defaults = {
		'imageshack.email': '',
		'imageshack.password': '',
	}
	def __init__(self, configmanager):
		self.configmanager = configmanager

	def store(self, filepath):
		email = self.configmanager['imageshack.email']
		password = self.configmanager.get_password('imageshack.password')
		cj = cookielib.CookieJar()
		upload_opener = urllib2.build_opener(MultipartDataHandler, urllib2.HTTPCookieProcessor(cj))
		if email and password:
			login_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			result = login_opener.open('http://imageshack.us/auth.php', urlencode({
				'username': email,
				'password': password
			}))
			if result.read() != 'OK':
				# Login error.
				print 'Login error. Continuing anyway'
				pass
			result.close()
		data = {
			'MAX_FILE_SIZE': 13145728,
			'refer': 'no_js_',
			'optimage': 'resample',
			'optsize': 'resample',
			'rembar': 0,
			'brand': '',
			'fileupload': open(filepath)
		}
		result = upload_opener.open('http://ufo.imageshack.us', data)
		# Get the redirect location
		new_location = result.url
		return self._get_url_from_result_url(new_location)

	def _get_url_from_result_url(self, result_url):
		"""Little utility function to get the real URL from the redirect we're given"""
		path = result_url.split('&l=')[1]
		server = path.split('/')[0]
		url = 'http://%s.imageshack.us/%s' % (server, path)
		return url
