import os
class WebStorage(object):
	"""
	An interface for defining web storage services for use with snappy.
	"""
	def __init__(self, configmanager):
		configmanager.settings.defaults.update(self.defaults)

	def store(self, filepath):
		"""Stores the capture, and returns its URL or location."""
		pass

def list_sharing_services():
	services_parent = __import__('snappy.backend', fromlist=['httpstorage']).httpstorage
	services_parent_dir = os.path.dirname(services_parent.__file__)
	services = {}
	for service in os.listdir(services_parent_dir):
		if service.split('.')[-1] == 'py' and service[:2] != '__':
			service = service.split('.')[0]
			service_module = getattr(__import__('snappy.backend.httpstorage', fromlist=[service]), service)
			for key, value in service_module.__dict__.iteritems():
				if key.lower() == service.lower() + 'storage':
					services[key] = value
	return services

def get_sharing_service_from_conf(configmanager):
	module_name = configmanager.settings['sharing.sharingservice']
	sharing_module = getattr(__import__('snappy.backend.httpstorage', fromlist=[module_name]), module_name)
	for key, value in sharing_module.__dict__.iteritems():
		if key.lower() == module_name.lower() + 'storage':
			return value(configmanager)
	raise NameError
