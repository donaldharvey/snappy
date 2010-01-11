import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import time
import os
import gst
from snappy.ui.gtk.dialogs.organiser import OrganiserDialog
from snappy.ui.gtk.keybindings import KeyBindingManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.ui.gtk.dialogs.preferences import Preferences
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

	def hello(self, widget, data=None):
		print 'Hi, world'

	def capture(self, widget, from_menu=False, type='area'):
		if from_menu:
			# Gives enough time for the menu to fade out before grabbing screenshot.
			time.sleep(0.5)
		capture_function = getattr(actions, 'capture_%s' % type)
		result = capture_function()
		if result is not None:
			# Play an alert sound.
			self.player.set_state(gst.STATE_PLAYING)
		notification = pynotify.Notification('Image uploaded', 'Snappy uploaded your screenshot to %s.' % result)
		notification.show()

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
			action = getattr(actions, action_name)
			KeyBindingManager().add_binding_from_string(binding, action)

		self.statusicon = gtk.StatusIcon()
		icon_file = os.path.join(os.path.dirname(__file__), "../../../resources/snappy24.png")
		print icon_file
		self.statusicon.set_from_file(icon_file)
		#set_from_file(icon_file) #FIXME: change to /usr/share/icons when installed?
		uimanager = gtk.UIManager()
		self.actiongroup = gtk.ActionGroup('MenuActions')
		self.actiongroup.add_actions([
			('preferences', gtk.STOCK_PREFERENCES, '_Preferences...', None, None, self.preferences),
			('about', gtk.STOCK_ABOUT, '_About...', None, None, self.about),
			('quit', gtk.STOCK_QUIT, '_Quit', None, None, self.destroy),
		])
		capture_actions = {
			'area': gtk.Action('capture_area', 'Capture _Area', None, gtk.STOCK_ABOUT),
			'window': gtk.Action('capture_window', 'Capture Active _Window', None, gtk.STOCK_ABOUT),
			'screen': gtk.Action('capture_screen', 'Capture Full _Screen', None, gtk.STOCK_ABOUT),
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

				<separator name="sep2" />

				<menuitem action="preferences" />
				<menuitem action="about" />
				<menuitem action="quit" />
			</popup>
		</ui>
		''')
		menu = uimanager.get_widget('ui/StatusIconMenu')
		## Now we connect these to their handlers.

		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", self.capture, False, 'area')

		# Set up gstreamer player to play alerts.
		audio_file = os.path.join(os.path.dirname(__file__), '../../../resources/finished.ogg')
		audio_file = os.path.abspath(audio_file)
		self.player = gst.parse_launch('filesrc location=%s ! oggdemux ! vorbisdec ! audioconvert ! gconfaudiosink' % audio_file)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self._gst_player_message)
		self.statusicon.set_visible(True)

if __name__ == '__main__':
	gtk.gdk.threads_init()
	statusicon = StatusIcon()
	statusicon.main()
