import gtk
import gobject
from snappy.backend.configmanagers import get_conf_manager
from snappy.backend.urlproviders import get_url_shortener_from_conf, list_url_shorteners
from snappy.backend.httpstorage import get_sharing_service_from_conf, list_sharing_services
import pdb
conf_manager = get_conf_manager()

# setup combo boxes
def setup_combo_box(container, widget_name):
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
		itemsliststore.append([item.nice_name, name])
		if item.__module__.split('.')[-1] == config_value:
			selected_item = row_number
		row_number += 1

	combo_box = container.get_widget_by_name(widget_name)
	combo_box.set_model(itemsliststore)
	cell = gtk.CellRendererText()
	combo_box.pack_start(cell, True)
	combo_box.add_attribute(cell, 'text', 0)
	combo_box.set_active(selected_item)

def startup(container):
	setup_combo_box(container, 'url_shortener_service')
	setup_combo_box(container, 'http_sharing_service')
	if container.get_widget_by_name('sharing_url_use_anonymous').get_active():
		container.get_widget_by_name('url_username').set_sensitive(False)
		container.get_widget_by_name('url_password').set_sensitive(False)
callbacks = {}
