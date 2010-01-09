import gtk
from snappy.backend.configmanagers import get_conf_manager
from snappy.ui.gtk.dialogs.preferences import PreferencesArea
conf_manager = get_conf_manager()
class MainAreaTab(PreferencesArea):
	def startup(self):
		print self.get_widget_by_name('quickshot')
		for name, binding in conf_manager.settings['keyboard_shortcuts.*'].iteritems():
			self.get_widget_by_name(name).set_text(binding)
		self.modifier_keyvals = (
			'Control_L',
			'Control_R',
			'Alt_L',
			'Alt_R',
			'Shift_L',
			'Shift_R',
			'Super_L',
			'Super_R',
			#more? needs testing...
		)
		self.modifiers_mask = 0
		for modifier in (gtk.gdk.CONTROL_MASK, gtk.gdk.SHIFT_MASK, gtk.gdk.MOD1_MASK,
			gtk.gdk.SUPER_MASK, gtk.gdk.HYPER_MASK):
			self.modifiers_mask |= modifier

	def kbd_entry_focus(self, widget, event, data=None):
		gtk.gdk.keyboard_grab(widget.window)
		global oldtext
		oldtext = widget.get_text()
		widget.set_editable(False)
		widget.set_text('[enter keyboard shortcut]')

	def kbd_entry_reset(self, widget, event, data=None):
		gtk.gdk.keyboard_ungrab()
		global oldtext
		if widget.get_text() == '[enter keyboard shortcut]':
			widget.set_text(oldtext)
		else:
			global conf_manager
			conf_manager.settings['keyboard_shortcuts.%s' % widget.get_name()] = widget.get_text()
		widget.set_editable(True)

	def kbd_entry_press(widget, event, data=None):
		# capture keypresses here
		k = gtk.gdk.keyval_name(event.keyval)
		if k in self.modifier_keyvals:
			return
		modifiers = event.state & self.modifiers_mask
		label = gtk.accelerator_name(event.keyval, modifiers)
		widget.set_text(label)
		print 'Key %s pressed.' % label
		gtk.gdk.keyboard_ungrab()

def kbd_entry_release(self, widget, event, data=None):
	pass

def replace_gnome_screenshot():
	pass

def unreplace_gnome_screenshot():
	pass