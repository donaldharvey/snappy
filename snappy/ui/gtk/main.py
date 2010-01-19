from snappy.backend.configmanagers import get_conf_manager
import gtk
def setup_defaults():
	conf_manager = get_conf_manager()
	defaults = {
		'sharing.sharingservice': 'tinypic',
		'sharing.shortener': 'none',
		'sharing.shortener_anonymous': 1,
		'keyboard_shortcuts.capture_area': '<Control>Print',
		'keyboard_shortcuts.capture_window': '<Control><Shift>Print',
		'keyboard_shortcuts.capture_screen': '<Super>Print',
		'use_temp_directory': 1,
	}
	conf_manager.settings.defaults.update(defaults)

def main(*args):
	setup_defaults()
	from snappy.ui.gtk.statusicon import StatusIcon
	gtk.gdk.threads_init()
	statusicon = StatusIcon()
	statusicon.main()
	#from snappy.ui.gtk.dialogs.organiser import OrganiserDialog
	#organiser = OrganiserDialog()
	#organiser.main()