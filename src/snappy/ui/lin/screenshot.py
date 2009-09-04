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
import os
import pygtk
pygtk.require('2.0')
import gtk
from datetime import datetime, date, time
class Screenshot:
	
	def _get_window_title(self, window):
		name = window.property_get('_NET_WM_NAME') #test this
		if name:
			return name[2]
		return 'Untitled Window'
	
	def _get_active_window(self):
		root = gtk.gdk.screen_get_default()
		active = root.get_active_window()
		return active
	
	def _get_current_window(self):
		current_window = self._get_active_window()
		if not current_window:
			current_window = gtk.gdk.window_at_pointer()
		current_window = current_window.get_toplevel()
		return current_window
	
	def grab_area(self, x, y, width, height):
		#TODO: REWRITE API CODE!
		#api.image.filename = "screenshot_" + datetime.now().strftime("%H-%M-%S_%d-%m-%y") + '.png'
		#api.image.path = api.tempdir + "screenshot_" + datetime.now().strftime("%H-%M-%S_%d-%m-%y") + '.png'
		#api.image.mimetype = "image/png"
		#api.image.title = "Screenshot taken at " + datetime.now().strftime("%H-%M-%S_%d-%m-%y")
		#api.image.size = (width, height)
		w = gtk.gdk.get_default_root_window()
		sz = w.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
		pb = pb.get_from_drawable(w,w.get_colormap(), x, y, 0, 0, width, height)
		#pb.save(api.image.path, 'png')
		#api.isvideo = False
		#print "Screenshot saved to " + api.image.path + "."
		return True
	
	def grab_window(self):
		window = self._get_current_window()
		title = self._get_window_title(window)
		print title
		width, height = window.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
		pb = pb.get_from_drawable(window, window.get_colormap(), 0, 0, 0, 0, width, height)
		pb.save('/home2/donald/.snappy/%s.png' % title, 'png')
		
#screenshot = Screenshot()
#screenshot.grab_window()

