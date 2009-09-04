#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
from snappy.backends.filesystem.backend import fsbackend

class OrganiserDialog():
	def hello(self, widget, data=None):
		print 'Hello universe.'
	def __init__(self, backend = fsbackend):
		self.backend = backend
		self.window = gtk.Window()
		self.window.connect('delete_event', lambda w: self.window.hide())
		
		vbox = gtk.VBox()
		
		
		def get_main_menu(self):
			window = self.window
			accelgroup = gtk.AccelGroup()
			item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accelgroup)
			item_factory.create_items(self.menu_items)
			window.add_accel_group(accelgroup)
			self.item_factory = item_factory
			return item_factory.get_widget("<main>")

		self.menu_items = (
			('/_File', 				None, None, 0, '<Branch>'),
			('/File/New', 			None, self.hello, 0, None),
			('/_Edit', 				None, None, 0, '<Branch>'),
			('/Edit/_Preferences',	None, self.hello, 0, None),
		)
		
		menubar = get_main_menu(self)
		vbox.pack_start(menubar, False, True, 0)
		
		hpane = gtk.HPaned()
		vbox.pack_start(hpane)
		
		self.window.add(vbox)
		
		self.window.show_all()
		self.window.show()
		# TODO: Add menubar XML
		
	def main(self):
		gtk.main()
		
if __name__ == '__main__':
	organiser = OrganiserDialog()
	organiser.main()