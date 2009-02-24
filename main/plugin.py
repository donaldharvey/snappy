#!/usr/bin/env python
def listplugins(plugindir):
	import os
	pluginlist = []
	for f in os.listdir(plugindir):
		if os.path.isdir(os.path.join(plugindir, f)):
			pluginlist.append(f)
	pluginlist.sort()
	print pluginlist
class Plugin:
	###PROPERTIES###
	fullname = "" 				# The full name of the plugin (e.g. ImageShack uploader)
	author = "" 				# Author name, obviously!
	website = ""				# Plugin website
	description = "" 			# The full description of the plugin.
	callback = None 			# The callback to execute after the button in actions.py is pressed
	icon = "" 					# The icon filename (MUST be a PNG!)
	class Settings:
		_settingsdict = {}
		def add(self, key, value):
			if not key in self._settingsdict:
				self._settingsdict[key] = value
				return key
			else:
				return False
			
		def remove(self, key):
			if key in self._settingsdict:
				del self._settingsdict[key]
				return True
			else:
				return False
		
		def get(self, key):
			if key in self._settingsdict:
				return self._settingsdict[key]
			else:
				return False
		
		def set(self, key, value):
			if key in self._settingsdict:
				self._settingsdict[key] = value
				return key
			else:
				return False
	settings = Settings()
	def __init__(self, callbackname):
		self.callback = callbackname

	def setproperty(self, key, value):
		if key == 'fullname':
			self.fullname = value
		elif key == 'author':
			self.author = value
		elif key == 'description':
			self.description = value
		elif key == 'icon':
			self.icon = value
		else:
			print 'No such property.'
	
def dothisnow(plugin):
	print "Hi!"
	print plugin.fullname
plugin = Plugin(dothisnow)
plugin.setproperty('fullname', 'An Awesome Plugin')
plugin.settings.add('foo', 'bar')
plugin.callback(plugin)

listplugins('../plugins/')
	