#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
from snappy.backends.filesystem.backend import fsbackend

class OrganiserDialog():
	def __init__(self, backend):
		self.backend = fsbackend
		self.window = gtk.Window()
		self.window.connect('delete_event', lambda w: self.window.hide())
		menubar = gtk.MenuBar()
		
	def main(self):
		gtk.main()