import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pynotify
import time
import os
import gst
import webbrowser
import platform
# Some of the snappy absolute imports are at the bottom of the file due to a
# circular import issue. I'll have to separate the notification code better
# somehow; this'll do for now.
from snappy.utils import Singleton

class SimpleGTKStatusIcon(gobject.GObject):
	__gsignals__ = {
		'activate': (gobject.SIGNAL_ACTION, gobject.TYPE_NONE, ()),
		'popup_menu': (gobject.SIGNAL_ACTION, gobject.TYPE_NONE, (gobject.TYPE_INT, gobject.TYPE_INT))
	}
	"""
	A status icon class with only a few simple methods.
	I created this primarly to be subclassed by the Win32StatusIcon class which
	I've had to write from the ground up.
	"""
	def __init__(self):
		self._statusicon = gtk.StatusIcon()
		pynotify.init('Snappy screen capture')
		self._statusicon.connect('activate', self._emit_proxy, 'activate')
		self._statusicon.connect('popup_menu', self._emit_proxy, 'popup_menu')
		self._statusicon.set_visible(True)
		super(SimpleGTKStatusIcon, self).__init__()

	def _emit_proxy(self, name='', *args, **kwargs):
		args = list(args)
		name = args.pop(-1)
		self.emit(name, *args, **kwargs)

	def set_icon_from_file(self, filename):
		return self._statusicon.set_from_file(filename)

	def notify(self, heading, content, icon=None):
		n = pynotify.Notification(heading, content)
		if icon:
			n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(icon))
		n.show()


class StatusIcon(object):
	def popup(self, widget, button, time, menu=None):
		"""Popup the menu."""
		if button == 3:
			if menu:
				menu.show_all()
				menu.popup(None, None, None, 3, time)
		pass

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def notify(self, *args, **kwargs):
		"""Display a notification to the user."""
		return self.statusicon.notify(*args, **kwargs)

	def about(self, widget, data=None):
		# For now, data is hardcoded in; later get these from setup.py
		aboutdialog = gtk.AboutDialog()
		aboutdialog.set_name('Snappy')
		aboutdialog.set_version('0.1 Beta')
		aboutdialog.set_copyright(u'Copyright \u00A9 2009-2010 Donald Harvey')
		aboutdialog.set_comments('A quick, customisable and easy-to-use screen capture app for Linux and Windows.')
		response = aboutdialog.run()
		aboutdialog.destroy()

	def capture(self, widget=None, from_menu=False, type='area'):
		"""
		The handler for all three types of screen capture.
		The type argument specifies the type of screen capture; one of area,
		fullscreen or active_window.
		As well as adding an item to the Recent Captures menu, this function
		also plays the alert sound and displays a notification.
		"""
		if from_menu:
			# Gives enough time for the menu to fade out before grabbing screenshot.
			time.sleep(0.5)
		capture_function = getattr(actions, 'capture_%s' % type)
		result = capture_function()
		print result
		if result is not None:
			# If the result is None, the user must have cancelled the capture.
			def menuitem_cb(widget, data=None):
				"""Callback to open the capture in a browser window."""
				url = widget.get_child().get_text().split(' at ')[0]
				webbrowser.open(url, new=2) # open url in a new tab

			# Play an alert sound.
			self.player.play()
			icon = os.path.join(PATHS['DATA_PATH'], 'uploaded.svg')
			self.notify('Image uploaded', 'Snappy uploaded your screenshot to %s.' % result, icon)
			if not self.recent_captures.props.sensitive:
				self.recent_captures.set_sensitive(True)
				# For some reason the UI manager adds an 'Empty' menuitem to the RecentCaptures menu.
				# The following code removes it.
				child = self.recent_captures.get_submenu().get_children()[1]
				if child.get_child().get_text() == 'Empty':
					self.recent_captures.get_submenu().remove(child)
			# Add a menuitem and connect it to the URL-opening handler above.
			menuitem = gtk.MenuItem('%s at %s' % (result, time.strftime('%H:%M')))
			menuitem.connect('activate', menuitem_cb)
			self.recent_captures.get_submenu().insert(menuitem, 0)


	def preferences(self, widget, data=None):
		Preferences().main()

	def main(self):
		"""Start up the KeyBindingManager and the gtk main loop."""
		KeyBindingManager().start()
		gtk.main()

	def __init__(self):
		mgr = get_conf_manager()
		bindings = mgr['keyboard_shortcuts.*']
		for action_name, binding in bindings.iteritems():
			# Set up the global key bindings.
			action = action_name.split('_', 1)[1]
			KeyBindingManager().add_binding_from_string(binding, self.capture, (None, False, action))

		self.statusicon = SimpleGTKStatusIcon()
		icon_file = os.path.join(PATHS['ICONS_PATH'], 'snappy24.png')
		print icon_file
		self.statusicon.set_icon_from_file(icon_file)

		# Set up the status icon menu with capture MenuItems
		# and a 'Recent Captures' menu.
		# It might be a good idea to move this out to a GtkBuilder file sometime.
		uimanager = gtk.UIManager()
		self.actiongroup = gtk.ActionGroup('MenuActions')

		self.actiongroup.add_actions([
			('recent_captures', None, '_Recent Captures', None, None, None),
			('preferences', gtk.STOCK_PREFERENCES, '_Preferences...', None, None, self.preferences),
			('about', gtk.STOCK_ABOUT, '_About...', None, None, self.about),
			('quit', gtk.STOCK_QUIT, '_Quit', None, None, self.destroy),
		])
		capture_actions = {
			'area': gtk.Action('capture_area', 'Capture _Area', None, None),
			'window': gtk.Action('capture_window', 'Capture Active _Window', None, None),
			'screen': gtk.Action('capture_screen', 'Capture Full _Screen', None, None),
		}
		for name, action in capture_actions.iteritems():
			action.connect('activate', self.capture, True, name)
			self.actiongroup.add_action(action)

		uimanager.insert_action_group(self.actiongroup, 0)
		accelgroup = uimanager.get_accel_group()
		uimanager.add_ui_from_string('''
		<ui>
			<popup name="StatusIconMenu">
				<menuitem action="capture_area" />
				<menuitem action="capture_window" />
				<menuitem action="capture_screen" />

				<separator name="sep1" />
				<menu action="recent_captures" name="RecentCaptures" />
				<separator name="sep2" />
				<menuitem action="preferences" />
				<menuitem action="about" />
				<menuitem action="quit" />
			</popup>
		</ui>
		''')
		menu = uimanager.get_widget('ui/StatusIconMenu')

		self.recent_captures = uimanager.get_widget('ui/StatusIconMenu/RecentCaptures')
		self.recent_captures.set_sensitive(False)

		# Connect the menu signals to their handlers.
		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", self.capture, False, 'area')

		# Set up the audio player with the finished sound
		audio_file = os.path.join(PATHS['DATA_PATH'], 'finished.wav')
		audio_file = os.path.abspath(audio_file)
		self.player = AudioPlayer(audio_file)
		#self.statusicon.set_visible(True)
	__metaclass__ = Singleton

from snappy.ui.gtk.keybindings import KeyBindingManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.ui.gtk.dialogs.preferences import Preferences
from snappy.ui.audioplayer import AudioPlayer
from snappy.globals import PATHS
from snappy.ui.gtk import actions

if __name__ == '__main__':
	gtk.gdk.threads_init()
	statusicon = StatusIcon()
	statusicon.main()
