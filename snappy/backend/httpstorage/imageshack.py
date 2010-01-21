import urllib2
import httplib
import urlparse
import os
from snappy.backend.httpstorage import WebStorage
from snappy.utils import MultipartDataHandler

class ImageShackStorage(WebStorage):
	"""Uses ImageShack to store files online."""
	nice_name = 'ImageShack online storage'
	defaults = {
		'imageshack.username': '',
		'imageshack.password': '',
	}
	def __init__(self, configmanager):
		self.configmanager = configmanager

	def store(self, filepath):
		opener = urllib2.build_opener(MultipartDataHandler, urllib2.HTTPCookieProcessor)
		data = {
			'MAX_FILE_SIZE': 13145728,
			'refer': 'no_js_',
			'optimage': 'resample',
			'optsize': 'resample',
			'rembar': 0,
			'brand': '',
			'fileupload': open(filepath)
		}
		result = opener.open('http://ufo.imageshack.us', data)
		# Get the redirect location
		new_location = result.url
		return self._get_url_from_result_url(new_location)

	def _get_url_from_result_url(self, result_url):
		"""Little utility function to get the real URL from the redirect we're given"""
		path = result_url.split('&l=')[1]
		server = path.split('/')[0]
		url = 'http://%s.imageshack.us/%s' % (server, path)
		return url
