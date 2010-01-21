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
from tempfile import mkstemp
import time
from snappy.utils import Singleton
from snappy.backend.configmanagers import get_conf_manager
class ScreenshotManager(object):
	'''
	This class contains mainly backend code to capture screenshots.
	Its most important function is grab_area().
	'''
	__metaclass__ = Singleton
	def __init__(self):
		self.configmanager = get_conf_manager()
	def _get_window_title(self, window):
		'''Get a gdk.Window's title'''
		name = window.property_get('_NET_WM_NAME') #test this
		if name:
			return name[2]
		return 'Untitled Window'

	def _get_active_window(self):
		root = gtk.gdk.screen_get_default()
		current_window = root.get_active_window()
		if not current_window:
			current_window = gtk.gdk.window_at_pointer()
		current_window = current_window.get_toplevel()
		return current_window

	def _save_pixbuf_to_file(self, pb, filename=''):
		if int(self.configmanager['use_temp_directory']):
			filepath = mkstemp('.png')[1]
		else:
			# Get the directory and remove the file:// at the start of the path
			directory = self.configmanager['screenshot_directory'][7:]
			if not filename:
				filename = time.strftime('%a %d %b %Y at %H-%M-%S.png')
			filepath = os.path.join(directory, filename)
		pb.save(filepath, 'png')
		return filepath

	def grab_fullscreen(self):
		height = gtk.gdk.screen_height()
		width = gtk.gdk.screen_width()
		return self.grab_area(0, 0, width, height)

	def grab_area(self, x, y, width, height):
		w = gtk.gdk.get_default_root_window()
		sz = w.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
		pb = pb.get_from_drawable(w,w.get_colormap(), x, y, 0, 0, width, height)
		return pb

	def grab_window(self):
		window = self._get_active_window()
		title = self._get_window_title(window)
		width, height = window.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
		pb = pb.get_from_drawable(window, window.get_colormap(), 0, 0, 0, 0, width, height)
		return self._save_pixbuf_to_file(pb, filename=title)


screenshotmanager = ScreenshotManager()
#screenshot.grab_window()
