import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import time
import os
import gst
import webbrowser
from snappy.ui.gtk.keybindings import KeyBindingManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.ui.gtk.dialogs.preferences import Preferences
from snappy.globals import PATHS
from snappy.ui.audioplayer import AudioPlayer
import actions

class StatusIcon:
	def _gst_player_message(self, bus, message):
		if message.type == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif message.type == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "gStreamer Error: %s" % err, debug

	def popup(self, widget, button, time, menu=None):
		if button == 3:
			if menu:
				menu.show_all()
				menu.popup(None, None, None, 3, time)
		pass

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def about(self, widget, data=None):
		# For now, data is hardcoded in; later get these from setup.py
		self.aboutdialog = gtk.AboutDialog()
		self.aboutdialog.set_name('Snappy')
		self.aboutdialog.set_version('0.1 Beta')
		self.aboutdialog.set_copyright(u'Copyright \u00A9 2009-2010 Donald Harvey')
		self.aboutdialog.set_comments('A quick, customisable and easy-to-use screen capture app for Linux.')
		response = self.aboutdialog.run()
		self.aboutdialog.hide()
		del self.aboutdialog

	def capture(self, widget, from_menu=False, type='area'):
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
			notification = pynotify.Notification('Image uploaded', 'Snappy uploaded your screenshot to %s.' % result)
			notification.show()
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
			self.recent_captures.get_submenu().append(menuitem)


	def preferences(self, widget, data=None):
		Preferences().main()

	def main(self):
		KeyBindingManager().start()
		gtk.main()

	def __init__(self):
		pynotify.init('Snappy Screen Capture')
		mgr = get_conf_manager()
		bindings = mgr.settings['keyboard_shortcuts.*']
		for action_name, binding in bindings.iteritems():
			# Set up the global key bindings.
			action = getattr(actions, action_name)
			KeyBindingManager().add_binding_from_string(binding, action)

		self.statusicon = gtk.StatusIcon()
		icon_file = os.path.join(PATHS['ICONS_PATH'], 'snappy24.png')
		print icon_file
		self.statusicon.set_from_file(icon_file)

		# Set up the status icon menu with capture MenuItems
		# and a 'Recent Captures' menu.
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
		self.statusicon.set_visible(True)

if __name__ == '__main__':
	gtk.gdk.threads_init()
	statusicon = StatusIcon()
	statusicon.main()
