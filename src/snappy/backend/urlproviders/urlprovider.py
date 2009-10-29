class UrlProvider:
	'''
	This class provides URL shortening to various Snappy functions.
	It is designed for subclassing, so it is easy to make a shortener
	plugin. Look at the bit.ly class for a reference implementation.
	'''
	def __init__(self):
		self.lasturl = None

	def shorten(self, url):
		self.lasturl = url
		newurl = url
		return newurl

	def auth(self, details):
		pass