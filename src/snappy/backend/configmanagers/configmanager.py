from UserDict import DictMixin
class ConfigDict(DictMixin):
	def __init__(self):
		self.dict = dict()
	def __getitem__(self, key):
		self.dict.__getitem__(key)
	def __setitem__(self, key, value):
		self.dict.__setitem__(key, value)

class ConfigManager:
	def __init__(self):
		from snappy.backend.urlproviders.trim import UrlProvider
		self.urlprovider = UrlProvider()
		self.settings = ConfigDict()
		
	def store_password(self, key, password):
		self.settings[key] = password