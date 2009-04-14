#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import pynotify
from snappy.main.screenshot import screenshot
from snappy.main.areaselect import SelectArea
from snappy.main.actions import Actions
from snappy.main.api import api
import time
class StatusIcon:
	def popup(self, widget, button, time, data=None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, None, 3, time)
		pass
	def destroy(widget, data=None):
		gtk.main_quit()
	
	def keypress(self, widget, data=None):
		print "Oh hey, is this guy bothering you?"
	def main(self):
		gtk.main()
		
	def takeScreenshot(self, widget, statusicon):
	#print "The size of the window is %d x %d" % sz
		areaselect = SelectArea()
		areaselect.main()
		if not areaselect.escaped:
			screenshot.grabArea(areaselect.getselection('x'), areaselect.getselection('y'), areaselect.getselection('width'), areaselect.getselection('height'))
			actions = Actions(api.image)
			actions.main()
		else:
			print "User cancelled."
	def __init__(self):
		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_from_file("../resources/icon.png")
		menu = gtk.Menu()
		
		## Here be the menu item definitions.
		item_screenshot = gtk.MenuItem("Take screenshot")
		item_preferences = gtk.MenuItem("Preferences")
		item_exit = gtk.MenuItem("Exit")
		
		## Now we connect these to their handlers.
		item_screenshot.connect("activate", self.takeScreenshot, self.statusicon)
		
		#item_preferences.connect("activate", settingswindow) #This function doesn't exist yet!
		item_exit.connect_object("activate", self.destroy, menu)
		
		##And finally, add these to the menu.
		menu.append(item_screenshot)
		menu.append(item_preferences)
		menu.append(item_exit)
		
		item_screenshot.show()
		item_preferences.show()
		item_exit.show()
		
		menu.set_title('Popup example')
		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", self.takeScreenshot, self.statusicon)
		#self.statusicon.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		#self.statusicon.connect("button_press_event", self.keypress)

		#self.statusicon.connect("")
		self.statusicon.set_visible(True)
