def get_conf_manager():
	from platform import system
	platform = system().lower()[:3]
	if platform == 'win':
		# possibly use registry; for now, just use fileconfigmanger
		from fileconfigmanager import FileConfigManager
		return FileConfigManager()
	elif platform == 'mac':
		# TODO: investigate this.
		pass
	else:
		# use gconf and gnome-keyring in future; for now, just use fileconfigmanager
		from fileconfigmanager import FileConfigManager
		return FileConfigManager()