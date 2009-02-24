#!/usr/bin/env python
# This file is part of Snappy.
#
# Snappy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snappy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snappy.  If not, see <http://www.gnu.org/licenses/>.
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
	