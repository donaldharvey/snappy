import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import time
import os
import gst
from snappy.ui.lin.dialogs.organiser import OrganiserDialog
from snappy.ui.lin.keybindings import KeyBindingManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.ui.lin.dialogs.preferences import Preferences
import actions

class StatusIcon:
	def _gst_player_message(self, bus, message):
		if message.type == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif message.type == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "gStreamer Error: %s" % err, debug

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

	def quickshot(self, widget, data=None):
		result = actions.quickshot()
		if result is not None:
			# Play an alert sound.
			self.player.set_state(gst.STATE_PLAYING)

	def preferences(self, widget, data=None):
		Preferences().main()

	organiser = hello
	def main(self):
		# Keybinding code here.
		KeyBindingManager().start()
		gtk.main()


	def __init__(self):
		mgr = get_conf_manager()
		bindings = mgr.settings['keyboard_shortcuts.*']
		for action_name, binding in bindings.iteritems():
			action = getattr(actions, action_name)
			KeyBindingManager().add_binding_from_string(binding, action)

		self.statusicon = gtk.StatusIcon()
		icon_file = os.path.join(os.path.dirname(__file__), "../../../../resources/snappy24.png")
		print icon_file
		self.statusicon.set_from_file(icon_file)
		#set_from_file(icon_file) #FIXME: change to /usr/share/icons when installed?
		uimanager = gtk.UIManager()
		self.actiongroup = gtk.ActionGroup('MenuActions')
		self.actiongroup.add_actions([
			('organiser', gtk.STOCK_ABOUT, 'Show _Organiser...', None, None, self.hello),
			('quickshot', gtk.STOCK_ABOUT, 'Take _Quickshot', None, None, self.quickshot),
			('screenshot', gtk.STOCK_ABOUT, 'Take _Screenshot', None, None, self.hello),
			('screencast', gtk.STOCK_HELP, '_Capture Screencast', None, None, self.hello),
			('extensions', gtk.STOCK_PREFERENCES, '_Extension Manager...', None, None, self.hello),
			('preferences', gtk.STOCK_PREFERENCES, '_Preferences...', None, None, self.preferences),
			('about', gtk.STOCK_ABOUT, '_About...', None, None, self.hello),
			('quit', gtk.STOCK_QUIT, '_Quit', None, None, self.hello),
		])
		uimanager.insert_action_group(self.actiongroup, 0)
		accelgroup = uimanager.get_accel_group()
		uimanager.add_ui_from_string('''
		<ui>
			<popup name="StatusIconMenu">
				<menuitem action="organiser" />

				<separator name="sep1" />

				<menuitem action="quickshot" />
				<menuitem action="screenshot" />
				<menuitem action="screencast" />

				<separator name="sep2" />

				<menuitem action="extensions" />
				<menuitem action="preferences" />
				<menuitem action="about" />
				<menuitem action="quit" />
			</popup>
		</ui>
		''')
		menu = uimanager.get_widget('ui/StatusIconMenu')

		## Now we connect these to their handlers.

		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", self.quickshot)

		# Set up gstreamer player to play alerts.
		audio_file = os.path.join(os.path.dirname(__file__), '../../../../resources/finished.ogg')
		audio_file = os.path.abspath(audio_file)
		self.player = gst.parse_launch('filesrc location=%s ! oggdemux ! vorbisdec ! audioconvert ! gconfaudiosink' % audio_file)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self._gst_player_message)
		self.statusicon.set_visible(True)

if __name__ == '__main__':
	statusicon = StatusIcon()
	statusicon.main()
