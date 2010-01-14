import gtk
import gobject
from snappy.backend.configmanagers import get_conf_manager
from snappy.backend.urlproviders import get_url_shortener_from_conf, list_url_shorteners
from snappy.backend.httpstorage import get_sharing_service_from_conf, list_sharing_services
from snappy.ui.gtk.dialogs.preferences import PreferencesArea
from snappy.globals import PATHS
import pdb
import os
conf_manager = get_conf_manager()

class SharingWindow(PreferencesArea):
	toplevel = None
	def get_widget_by_name(self, name):
		fn = super(SharingWindow, self).get_widget_by_name.im_func
		return fn(self.toplevel, name)

	def close(self, widget=None, data=None):
		self.toplevel.hide()
		self.toplevel.destroy()

class SharingTab(PreferencesArea):
	def startup(self):
		self.get_toplevel()
		self.setup_combo_box('url_shortener_service')
		self.setup_combo_box('http_sharing_service')
		if self.get_widget_by_name('sharing_url_use_anonymous').get_active():
			self.get_widget_by_name('url_username').set_sensitive(False)
			self.get_widget_by_name('url_password').set_sensitive(False)

	def setup_combo_box(self, widget_name):
		#TODO: Sort out variable names and comment this function.
		if 'url_shortener' in widget_name:
			items = list_url_shorteners()
			config_value = conf_manager.settings['sharing.shortener']
		else:
			items = list_sharing_services()
			config_value = conf_manager.settings['sharing.sharingservice']
		itemsliststore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
		row_number = 0
		selected_item = -1
		for name, item in items.iteritems():
			module_name = item.__module__.split('.')[-1]
			if module_name == 'urlproviders':
				module_name = 'none'
			itemsliststore.append([item.nice_name, module_name])
			if module_name == config_value:
				selected_item = row_number
			row_number += 1

		combo_box = self.get_widget_by_name(widget_name)
		combo_box.set_model(itemsliststore)
		cell = gtk.CellRendererText()
		combo_box.pack_start(cell, True)
		combo_box.add_attribute(cell, 'text', 0)
		combo_box.set_active(selected_item)

	def shortener_settings_change(self, widget, data=None):
		if widget.get_name() == 'sharing_url_use_anonymous':
			self.get_widget_by_name('url_username').set_sensitive(widget.get_active() == False)
			self.get_widget_by_name('url_password').set_sensitive(widget.get_active() == False)
		elif widget.get_name() == 'url_username':
			conf_manager.settings['sharing.shortener_username'] = widget.get_value()
		elif widget.get_name() == 'url_password':
			conf_manager.set_password('sharing.shortener_password', widget.get_value())

	def change_sharing_combo(self, widget, data=None):
		model = widget.get_model()
		if widget.get_name() == 'http_sharing_service':
			settingname = 'sharing.sharingservice'
		else:
			settingname = 'sharing.shortener'
		conf_manager.settings[settingname] = model.get_value(widget.get_active_iter(), 1)

	def open_sharing_window(self, widget, data=None):
		combo = self.get_widget_by_name('http_sharing_service')
		model = combo.get_model()
		name = model.get_value(combo.get_active_iter(), 1)
		area_module = getattr(__import__('snappy.ui.gtk.dialogs.preferences.sharing', fromlist=[name]), name)
		print dir(area_module)
		for key, value in area_module.__dict__.iteritems():
			clean_name = name.replace('_', '').lower()
			print clean_name
			print key
			if key.lower() == clean_name + 'window':
				self.sharing_window_methods = value()
		builder = gtk.Builder()
		path = os.path.join(PATHS['DATA_PATH'], 'glade', 'preferences', 'sharing', name + '.glade')
		builder.add_from_file(path)
		window = builder.get_object(name + '_window')
		builder.connect_signals(self.sharing_window_methods)
		del builder
		self.sharing_window_methods.toplevel = window
		self.sharing_window_methods.startup()
		parent_win = self.get_toplevel()
		window.set_transient_for(parent_win)
		window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
		window.show()