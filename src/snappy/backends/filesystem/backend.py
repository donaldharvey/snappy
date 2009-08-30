from snappy.backends.backend import Backend
import os
import sys
import unittest
from snappy.db.model import Model
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
	
	def prepareSQL(self, Model):
		for table in vars(Model):
			if table[1] == '_':
				continue
			Table = getattr(Model, table)
			print table, 'table:'
			tableobj = Table()
			fields = vars(tableobj)
			for field in fields:
				if field[0] == '_':
					# don't include private or built-in instance variables in
					# the field list
					continue
				print '....' + field, getattr(tableobj, field)
				
			tablesql = ('create table (?)', (fields)
	def _sqliteCreateDB(self, dbpath, sql, returnConnection = False):
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
		try:
			c = connection.cursor()
			c.execute(sql)
			connection.commit()
		except sqlite3.OperationalError:
			# sounds like DB already exists; unlink and add again for now.
			connection = False
			os.remove(dbpath)
			connection = sqlite3.connect(dbpath)
			c = connection.cursor()
			c.execute(sql)
			connection.commit()
		finally:
			if not returnConnection:
				return dbpath
			return connection
		
	class dbObject(Backend.dbObject):
		'''
		A set of methods allowing one to get, set and delete values from the database.
		This class uses model.py to get its model definitions.
		'''
		import sqlite3
		
		def __init__(self, connection, model=Model):
			self.dbconnection = connection
			self.model = model
			
		def get(self, objtype, identifier):
			'''
			Returns a database object when supplied with an identifier and object type.
			'''
			connection = self.dbconnection
			c = connection.cursor()
			try:
				ModelObj = getattr(self.model, objtype.lower().capitalize())
				obj = ModelObj()
				c = connection.cursor()
				print 'select * from %s where %s=%s' % (objtype.lower(), obj.pk, identifier)
				c.execute('select * from image')
				for row in c:
					print row
				return True
			except Exception as e:
				print e
				return False
			
		def set(self, objtype, data):
			if not type(data) == dict:
				raise __builtins__.TypeError
				return False
			connection = self.dbconnection
			c = connection.cursor()
			
			
			
			return data
		def delete(self, objtype, identifier):
			return identifier
		
	
	def __init__(self):
		sql = "create table image(title text, content text)"
		self.appdatadir = self._appDataDir()
		dbpath = os.path.join(self.appdatadir, 'database.db')
		print dbpath
		sqlite = self._sqliteCreateDB(dbpath, sql, True)
		self.dbobject = self.dbObject(sqlite)
		print 'Preparing SQL:'
		self.prepareSQL(Model)
		print 'dbobj get returned ' + str(self.dbobject.get('image', 0))