# Loosely based on https://www.siafoo.net/snippet/239
import gtk
import gobject
import threading
import platform
if platform.system() != 'Windows':
	from Xlib.display import Display
	from Xlib import X
else:
	import pythoncom
	import pyHook

from snappy.utils import Singleton

class KeyBindingManager(threading.Thread):
	"""
	An Xlib-based global key bindings manager.
	"""
	__metaclass__ = Singleton

	def __init__(self):
		super(KeyBindingManager, self).__init__()
		self.daemon = True
		self.display = Display()
		self.root = self.display.screen().root
		self._binding_map = {}

		self.known_modifiers_mask = 0
		gdk_modifiers = (gtk.gdk.CONTROL_MASK, gtk.gdk.SHIFT_MASK, gtk.gdk.MOD1_MASK,
			gtk.gdk.MOD2_MASK, gtk.gdk.MOD3_MASK, gtk.gdk.MOD4_MASK, gtk.gdk.MOD5_MASK,
			gtk.gdk.SUPER_MASK, gtk.gdk.HYPER_MASK)
		for mod in gdk_modifiers:
			self.known_modifiers_mask |= mod


	def add_binding_from_string(self, binding_string, action, args=(), kwargs={}):
		"""
		Add a key binding from an accelerator string.
		Uses gtk.accelerator_parse to parse the string; according to the docs,
		this is "fairly liberal" and "allows abbreviations such as '<Ctrl>' and '<Ctl>'".
		"""
		print 'Adding', binding_string
		keyval, modifiers = gtk.accelerator_parse(binding_string)
		print modifiers
		action = (action, args, kwargs)
		keycode = gtk.gdk.keymap_get_default().get_entries_for_keyval(keyval)[0][0]
		self._binding_map[(keycode, modifiers)] = action
		self.regrab()

	def grab(self):
		for (keycode, modifiers) in self._binding_map.keys():
			self.root.grab_key(keycode, int(modifiers), True, X.GrabModeAsync, X.GrabModeSync)

	def ungrab(self):
		for (keycode, modifiers) in self._binding_map.keys():
			self.root.ungrab_key(keycode, modifiers, self.root)

	def regrab(self):
		self.ungrab()
		self.grab()


	def _action_idle(self, action):
		gtk.gdk.threads_enter()
		action, args, kwargs = action
		gobject.idle_add(action, args, kwargs)
		gtk.gdk.threads_leave()
		return False

	def run(self):
		self.running = True
		wait_for_release = False
		while self.running:
			event = self.display.next_event()
			if event.type == X.KeyPress and not wait_for_release:
				keycode = event.detail
				modifiers = event.state & self.known_modifiers_mask
				try:
					action = self._binding_map[(keycode, modifiers)]
				except KeyError:
					# This key binding isn't handled by Snappy.
					self.display.allow_events(X.ReplayKeyboard, event.time)
				else:
					# Get the action ready for when the key combo is released
					wait_for_release = True
					self.display.allow_events(X.AsyncKeyboard, event.time)
					self._upcoming_action = (keycode, modifiers, action)

			elif event.type == X.KeyRelease and wait_for_release and event.detail == self._upcoming_action[0]:
				# The user has released the key combo; run the queued action
				wait_for_release = False
				action = self._upcoming_action[2]
				del self._upcoming_action
				gobject.idle_add(self._action_idle, action)
				self.display.allow_events(X.AsyncKeyboard, event.time)

			else:
				self.display.allow_events(X.ReplayKeyboard, event.time)

	def stop(self):
		self.running = False
		self.ungrab()
		self.display.close()

class WinKeyBindingManager(KeyBindingManager):
	"""
	A Windows key binding manager that uses Win32 hooks (via PyHook).
	"""
	def __init__(self):
		super(super(WinKeyBindingManager, self)).__init__()
		self.hook_manager = pyHook.HookManager()
		self.hook_manager.KeyUp = self.handle_keypress

	def add_binding_from_string(self, binding_string, action):
		pass

	def handle_keypress(self, event):
		pass


if __name__ == '__main__':
	gtk.gdk.threads_init()
	kbm = KeyBindingManager()
	def t(*args, **kwargs):
		print 'Called!'
	kbm.add_binding_from_string('<Control><Shift>dollar', t)
	kbm.start()
	gtk.main()