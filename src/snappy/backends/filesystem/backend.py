from snappy.backends.backend import Backend
import os, sys
from snappy.db import model
class filesystem(Backend):
	'''
	Snappy's default backend - storing images/videos in the filesystem,
	and metadata in an sqlite3 database.
	Requires python 2.5 for the sqlite3 module.
	'''
	
	def _appDataDir(self, appname='snappy'):
		'''
		Returns (and creates if it does not exist) the application's data directory for all 3 major platforms.
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
	
	def _sqliteCreateDB(self, dbpath, sql):
		'''
		Creates an sqlite DB at location dbpath.
		Requires python 2.5 for sqlite3 module.
		'''
		import sqlite3
		print dbpath
		try:
			connection = sqlite3.connect(dbpath)
		except Exception:
			print 'Python sqlite import failed.'
			return False
		#TODO: OOP/ORM-ise this later?
		try:
			c = connection.cursor()
			c.execute(sql)
			connection.commit()
			c.close()
		except Exception:
			return False
		else:
			return dbpath
		
	def __init__(self):
		sql = "create table test(title text, content text)"
		self.appdatadir = self._appDataDir()
		dbpath = os.path.join(self.appdatadir, 'database.db')
		print dbpath
		self._sqliteCreateDB(dbpath, sql)
		
	class dbObject(object):
		def __get__(self, type, identifier):
			import __builtin__
			for obj in vars(model):
				if type == repr(obj):
					themodel = obj
			try:
				print repr(themodel)
			except Exception:
				print 'The supplied type does not exist.'
				return False
			pass
	
#test code
backend = filesystem()