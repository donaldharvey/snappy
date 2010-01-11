import os
class UrlProvider:
	'''
	This class provides URL shortening to various Snappy functions.
	It is designed for subclassing, so it is easy to make a shortener
	plugin. Look at the bit.ly class for a reference implementation.
	'''
	nice_name = 'None'
	def __init__(self, configmanager):
		self.configmanager = configmanager
		self.lasturl = None

	def shorten(self, url):
		self.lasturl = url
		newurl = url
		return newurl

	def auth(self, details):
		pass

def list_url_shorteners():
	shorteners_parent = __import__('snappy.backend', fromlist=['urlproviders']).urlproviders
	shorteners_parent_dir = os.path.dirname(shorteners_parent.__file__)
	shorteners = {}
	for shortener in os.listdir(shorteners_parent_dir):
		if shortener.split('.')[-1] == 'py':
			shortener = shortener.split('.')[0]
			if shortener == '__init__':
				shorteners['UrlProvider'] = UrlProvider
			else:
				shortener_module = getattr(__import__('snappy.backend.urlproviders', fromlist=[shortener]), shortener)
				for key, value in shortener_module.__dict__.iteritems():
					if key.lower() == shortener.lower() + 'urlprovider':
						shorteners[key] = value
	return shorteners

def get_url_shortener_from_conf(configmanager):
	module_name = configmanager.settings['sharing.shortener']
	if module_name == 'none':
		return UrlProvider(configmanager)
	else:
		shortener_module = getattr(__import__('snappy.backend.urlproviders', fromlist=[module_name]), module_name)
		for key, value in shortener_module.__dict__.iteritems():
			if key.lower() == module_name.lower() + 'urlprovider':
				return value(configmanager)
	raise NameError