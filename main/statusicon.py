#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import pynotify
from snappy.main.screenshot import screenshot
from snappy.main.areaselect import SelectArea
from snappy.main.actions import Actions
from snappy.main.api import api
from snappy.main.keybindings import GlobalKeyBinding
import gconf
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
		keybinding = GlobalKeyBinding('<Control><Shift><Alt>Print')
		keybinding.connect('activate', self.takeScreenshot, self.statusicon, False)
		keybinding.grab()
		keybinding.start()
		gtk.main()
		
	def takeScreenshot(self, widget, statusicon, isfullscreen):
	#print "The size of the window is %d x %d" % sz
		if not isfullscreen:
			areaselect = SelectArea()
			areaselect.main()
			if not areaselect.escaped:
				screenshot.grabArea(areaselect.getselection('x'), areaselect.getselection('y'), areaselect.getselection('width'), areaselect.getselection('height'))
				actions = Actions(api.image)
				actions.main()
				url = actions.plugin.callback(actions.plugin)
				print url
			else:
				print "User cancelled."
		else:
			time.sleep(1)
			w = gtk.gdk.get_default_root_window()
			width, height = w.get_size()
			screenshot.grabArea(0, 0, width, height)
			actions = Actions(api.image)
			actions.main()
	def __init__(self):
		gtk.threads_init()
		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_from_file("../resources/icon.png")
		menu = gtk.Menu()
		client = gconf.client_get_default()
#		client.add_dir('/apps/snappy/keybindings', gconf.CLIENT_PRELOAD_NONE)
		client.set_string('/apps/snappy/keybindings/screengrab-area', '<Shift>Print')
		
		## Here be the menu item definitions.
		item_captureArea = gtk.MenuItem("Capture Area")
		item_captureFullscreen = gtk.MenuItem("Capture Entire Screen")
		item_preferences = gtk.MenuItem("Preferences")
		item_exit = gtk.MenuItem("Exit")
		
		## Now we connect these to their handlers.
		item_captureArea.connect("activate", self.takeScreenshot, self.statusicon, False)
		item_captureFullscreen.connect("activate", self.takeScreenshot, self.statusicon, True)
		
		#item_preferences.connect("activate", settingswindow) #This function doesn't exist yet!
		item_exit.connect_object("activate", self.destroy, menu)
		
		##And finally, add these to the menu.
		menu.append(item_captureArea)
		menu.append(item_captureFullscreen)
		menu.append(item_preferences)
		menu.append(item_exit)
		
		item_captureArea.show()
		item_captureFullscreen.show()
		item_preferences.show()
		item_exit.show()
		
		menu.set_title('Popup example')
		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", self.takeScreenshot, self.statusicon, False)
		#self.statusicon.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		#self.statusicon.connect("button_press_event", self.keypress)

		#self.statusicon.connect("")
		self.statusicon.set_visible(True)
