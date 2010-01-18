from snappy.backend.urlproviders import UrlProvider
from urllib import urlopen, quote
try:
	import json
except ImportError:
	import simplejson as json
import socket

class TrimUrlProvider(UrlProvider):
	nice_name = 'Tr.im'
	api_url = 'http://api.tr.im/api/trim_url.json'
	def shorten(self, url):
		socket.setdefaulttimeout(7.5)
		clean_url = quote(url)
		f = urlopen(self.api_url + '?url=' + clean_url)
		response = json.loads(f.read())
		f.close()
		return response['url']