#!/usr/bin/env python
# Copyright (C) 2009 Donald S. F. Harvey
#
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
	guicallback = None			# The event to add all GUI widgets to the plugin settings dialog.
	icon = "" 					# The icon filename (MUST be a PNG!)
	settings = {}
	returnsurl = True
	def __init__(self, callbackname, guicallbackname):
		self.callback = callbackname
		self.guicallback = guicallbackname

	def setproperty(self, key, value):
		if key == 'fullname':
			self.fullname = value
		elif key == 'author':
			self.author = value
		elif key == 'description':
			self.description = value
		elif key == 'icon':
			self.icon = value
		elif key == 'returnsurl':
			self.returnsurl = value
		else:
			print 'No such property.'
	
#def dothisnow(plugin):
#	print "Hi!"
#	print plugin.fullname
#plugin = Plugin(dothisnow, dothisnow)
#plugin.setproperty('fullname', 'An Awesome Plugin')
#plugin.settings.add('foo', 'bar')
#plugin.callback(plugin)

#listplugins('../plugins/')
	