from configmanager import ConfigManager, ConfigDict
from ConfigParser import ConfigParser
import sys
import os

def app_data_dir(appname='snappy'):
	'''
	Returns (and creates if it does not exist) the application's data directory for all 3 major platforms.
	Based on http://[stackoverflow url].
	'''
	if sys.platform == 'darwin':
		from AppKit import NSSearchPathForDirectoriesInDomains
		# http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
		# NSApplicationSupportDirectory = 14
		# NSUserDomainMask = 1
		# True for expanding the tilde into a fully qualified path
		appdata = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], appname)
	elif sys.platform == 'win32':
		appdata = os.path.join(environ['APPDATA'], appname)
	else:
		appdata = os.path.expanduser(os.path.join("~", "." + appname))

	if not os.access(appdata, os.F_OK):
		os.mkdir(appdata)
	return appdata

class FileConfigManager(ConfigManager):
	def __init__(self):
		super(GnomeConfigManager, self).__init__()
		self.settings = FileConfigDict()

class FileConfigDict(ConfigDict):
	def __init__(self):
		super(FileConfigDict, self).__init__()
		self.filename = os.path.join(app_data_dir(), 'settings.cfg')
		self.parser = ConfigParser()
		self.parser.readfp(open(self.filename, 'r+'))

	def __getitem__(self, key):
		section, option = key.split('.', 1)
		return self.parser.get(section, option)

	def __setitem__(self, key, value):
		section, option = key.split('.', 1)
		if not self.parser.has_section(section):
			self.parser.add_section(section)
		self.parser.set(section, option, value)

	def __delitem__(self, key):
		section, option = key.split('.', 1)
		self.parser.remove_option(section, option)

	def keys(self):
		keys = ()
		for section in self.parser.sections():
			for option in self.parser.items(section):
				keys.append(section + '.' + option)
		return keys