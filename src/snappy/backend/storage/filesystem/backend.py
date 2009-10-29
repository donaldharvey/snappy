from snappy.backends.backend import Backend
import os
import sys
import unittest
from snappy.backend.db import models
from snappy.backend.configmanagers.fileconfigmanager import app_data_dir
class Filesystem(Backend):
	'''
	Snappy's default backend - storing images/videos in the filesystem,
	and metadata in an sqlite3 database.
	Requires python 2.5 for the sqlite3 module.
	'''

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
				identifier = obj.id
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


	def __init__(self):
		self.appdatadir = app_data_dir()
		dbpath = os.path.join(self.appdatadir, 'database.db')
		print dbpath
		print self._sqliteCreateDB(dbpath, models.Model)
		self.dbobject = self.dbObject(models.Model)
		self.dbobject.set('category', {
			'name': 'Snappy organiser',
			'parent': 0,
			'icon': 'default:default.png'
		})
		self.dbobject.set('category', {
			'name': 'Windows',
			'parent': 5,
			'icon': 'default:default.png'
		})
		self.dbobject.set('category', {
			'name': 'Mac OS X',
			'parent': 5,
			'icon': 'default:default.png'
		})
		self.dbobject.set('category', {
			'name': 'Ubuntu',
			'parent': 5,
			'icon': 'default:default.png'
		})
		self.dbobject.set('category', {
			'name': 'Dialogs',
			'parent': 1,
			'icon': 'default:default.png'
		})
fsbackend = Filesystem()