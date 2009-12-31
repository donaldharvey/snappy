import gtk
import gobject
from snappy.backend.configmanagers import get_conf_manager
from snappy.backend.urlproviders import trim
import pdb
conf_manager = get_conf_manager()

def get_shorteners():
	shorteners_parent = __import__('snappy.backend', fromlist=['urlproviders']).urlproviders
	print shorteners_parent
	shorteners = {}
	for shortener in dir(shorteners_parent):
		if shortener[:2] != '__' and shortener != 'urlprovider':
			for key, value in getattr(shorteners_parent, shortener).__dict__.iteritems():
				if key.lower() == shortener.lower() + 'urlprovider':
					shorteners[key] = value
	return shorteners

def startup(widget):
	for name, binding in conf_manager.settings['sharing.*'].iteritems():
		pass
	shorteners = get_shorteners()
	shortenersliststore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
	for name, shortener in shorteners.iteritems():
		shortenersliststore.append([shortener.nice_name, name])
	shorteners_combo_box = widget.get_widget_by_name('url_shortener_service')
	shorteners_combo_box.set_model(shortenersliststore)
	cell = gtk.CellRendererText()
	shorteners_combo_box.pack_start(cell, True)
	shorteners_combo_box.add_attribute(cell, 'text', 0)

callbacks = {}
