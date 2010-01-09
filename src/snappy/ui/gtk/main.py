from snappy.backend.configmanagers import get_conf_manager
def setup_defaults():
	conf_manager = get_conf_manager()
	defaults = {
		'sharing.sharingservice': 'tinypic',
		'sharing.shortener': 'none',
		'keyboard_shortcuts.quickshot': '<Control>Print',
		'keyboard_shortcuts.screenshot': '<Control><Shift>Print',
		'keyboard_shortcuts.screencast': '<Super>Print',
	}
	conf_manager.settings.defaults.update(defaults)

def main(*args):
	setup_defaults()
	from snappy.ui.gtk.statusicon import StatusIcon
	statusicon = StatusIcon()
	statusicon.main()
	#from snappy.ui.gtk.dialogs.organiser import OrganiserDialog
	#organiser = OrganiserDialog()
	#organiser.main()