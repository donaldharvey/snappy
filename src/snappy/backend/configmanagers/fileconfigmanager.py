from configmanager import ConfigManager, ConfigDict
from ConfigParser import ConfigParser, NoSectionError
import sys
import os
from Crypto.Cipher import Blowfish #for password storage
from hashlib import sha1
from random import randrange

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
		super(FileConfigManager, self).__init__()
		self.settings = FileConfigDict()

	def _pad_pass(self, password):
		pad_bytes = 8 - (len(password) % 8)
		for i in range(pad_bytes - 1):
			password += chr(randrange(0, 256))
		# final padding byte; % by 8 to get the number of padding bytes
		bflag = randrange(6, 248)
		bflag -= bflag % 8 - pad_bytes
		password += chr(bflag)
		return password

	def _depad_pass(self, password):
		pad_bytes = ord(password[-1]) % 8
		if not pad_bytes:
			pad_bytes = 8
		return password[:-pad_bytes]

	def set_password(self, key, password):
		cryptkey = sha1(key).hexdigest()
		bf = Blowfish.new(cryptkey, Blowfish.MODE_ECB)
		encrypted_pass = bf.encrypt(self._pad_pass(password))
		del password
		self.settings[cryptkey] = encrypted_pass

	def get_password(self, key):
		cryptkey = sha1(key).hexdigest()
		bf = Blowfish.new(cryptkey, Blowfish.MODE_ECB)
		encrypted_pass = self.settings[cryptkey]
		decrypted_pass = self._depad_pass(bf.decrypt(encrypted_pass))
		return decrypted_pass

class FileConfigDict(ConfigDict):
	def __init__(self):
		super(FileConfigDict, self).__init__()
		self.filename = os.path.join(app_data_dir(), 'settings.cfg')
		if not os.path.exists(self.filename):
			open(self.filename, 'w').close()
		self.parser = ConfigParser()
		f = open(self.filename, 'r+')
		self.parser.readfp(f)
		f.close()

	def __getitem__(self, key):
		try:
			section, option = key.split('.', 1)
		except ValueError:
			section, option = 'misc', key
		return self.parser.get(section, option)

	def __setitem__(self, key, value):
		try:
			section, option = key.split('.', 1)
		except ValueError:
			section, option = 'misc', key
		if not self.parser.has_section(section):
			self.parser.add_section(section)
		self.parser.set(section, option, value)
		f = open(self.filename, 'w')
		self.parser.write(f)
		f.close()

	def __delitem__(self, key):
		try:
			section, option = key.split('.', 1)
		except ValueError:
			section, option = 'misc', key
		self.parser.remove_option(section, option)

	def keys(self):
		keys = list()
		for section in self.parser.sections():
			for option in self.parser.items(section):
				keys.append(section + '.' + option[0])
		return keys