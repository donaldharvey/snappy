from snappy.backends.backend import Backend
import os
import sys
import unittest
from snappy.db import models
class filesystem(Backend):
	'''
	Snappy's default backend - storing images/videos in the filesystem,
	and metadata in an sqlite3 database.
	Requires python 2.5 for the sqlite3 module.
	'''
	
	def _appDataDir(self, appname='snappy'):
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
	
	def _sqliteCreateDB(self, dbpath, model):
		model = models.Model()
		'''
		Creates/syncs an sqlite DB at location dbpath.
		Requires python 2.5 for sqlite3 module.
		'''
		try:
			import sqlobject
		except Exception:
			print 'Python sqlite import failed.'
			return False
		if os.path.exists(dbpath):
			os.remove(dbpath)
		print 'Attempting connection to', dbpath + '...'
		connectionpath = 'sqlite://' + dbpath
		connection = sqlobject.connectionForURI(connectionpath)
		sqlobject.sqlhub.processConnection = connection
		transaction = connection.transaction()
		print 'Vars:', dir(model)
		for table in dir(model): #FIXME: is there a better way to do this?
			if table[0] == '_':
				continue
			Table = getattr(model, table)
			Table.createTable()
		transaction.commit(close = True)
		return dbpath
		
	class dbObject(Backend.dbObject):
		'''
		A set of methods allowing one to get, set and delete values from the database.
		This class uses model.py to get its model definitions.
		'''
		
		def __init__(self, model = models.Model):
			self.model = model
			
		def get(self, objtype, identifier):
			'''
			Returns a database object when supplied with an identifier and object type.
			'''
			try:
				Table = getattr(self.model, objtype.lower().capitalize())
			except Exception: #FIXME: Change to a more specific exception
				return False
			return Table.get(identifier)
			
		def set(self, objtype, data, identifier=False):
			if not type(data) == dict:
				raise __builtins__.TypeError
				return False
			try:
				Table = getattr(self.model, objtype.lower().capitalize())
			except Exception: #FIXME: Change to a more specific exception
				return False
			if not identifier:
				obj = Table(**data)
			else:
				obj = Table.get(identifier)
				obj.set(data)
			return identifier
			
		def delete(self, objtype, identifier):
			try:
				Table = getattr(models.Model, objtype.lower().capitalize())
			except Exception: #FIXME: Change to a more specific exception
				return False
			obj = Table.get(identifier)
			del obj
			return True
		
	
	def __init__(self, osname = ""):
		sql = "create table image(title text, content text)"
		self.appdatadir = self._appDataDir()
		dbpath = os.path.join(self.appdatadir, 'database.db')
		print dbpath
		print self._sqliteCreateDB(dbpath, models.Model)
		self.dbobject = self.dbObject(models.Model)
		print self.dbobject.set('category', {
			'name': 'Awesome screenshots',
			'parent': None
		})
		print 'dbobj get returned ' + str(self.dbobject.get('category', 1))