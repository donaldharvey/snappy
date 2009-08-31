import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import time
from snappy.ui.lin.dialogs.organiser import OrganiserDialog
class StatusIcon:
	def popup(self, widget, button, time, data=None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, None, 3, time)
		pass
	
	def destroy(widget, data=None):
		gtk.main_quit()

	def hello(self, widget, data=None):
		print 'Hi, world'
		
	organiser = hello
	def main(self):
		# Keybinding code here.
		gtk.main()
		
	def __init__(self):
		gtk.threads_init()
		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_from_file("../../../../../resources/icon.png") #FIXME: change to /usr/share/icons when installed?
		uimanager = gtk.UIManager()
		self.actiongroup = gtk.ActionGroup('MenuActions')
		self.actiongroup.add_actions([
			('organiser', set_from_file('../../../../../resources/icon.png'), 'Show _Organiser...', None, None, self.hello),
			('quickshot', gtk.STOCK_ABOUT, 'Take _Quickshot', None, None, self.hello),
			('screenshot', gtk.STOCK_ABOUT, 'Take _Screenshot', None, None, self.hello),
			('screencast', gtk.STOCK_HELP, '_Capture Screencast', None, None, self.hello),
			('extensions', gtk.STOCK_PREFERENCES, '_Extension Manager...', None, None, self.hello),
			('about', gtk.STOCK_ABOUT, '_About...', None, None, self.hello),
			('quit', gtk.STOCK_QUIT, '_Quit', None, None, self.hello),
		])
		uimanager.insert_action_group(self.actiongroup, 0)
		accelgroup = uimanager.get_accel_group()
		uimanager.add_ui_from_file('statusiconmenu.xml')
		menu = uimanager.get_widget('ui/StatusIconMenu')
		#client = gconf.client_get_default()
		#client.add_dir('/apps/snappy/keybindings', gconf.CLIENT_PRELOAD_NONE)
		#client.set_string('/apps/snappy/keybindings/screengrab-area', '<Shift>Print')
		
		
		## Now we connect these to their handlers.
		
		#menu.set_title('Popup example')
		self.statusicon.connect("popup_menu", self.popup, menu)
		
		#self.statusicon.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		#self.statusicon.connect("button_press_event", self.keypress)

		#self.statusicon.connect("")
		self.statusicon.set_visible(True)

if __name__ == '__main__':
	statusicon = StatusIcon()
	statusicon.main()
