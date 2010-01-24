import os
from mimetypes import guess_type
import httplib
from snappy.ui.gtk.statusicon import StatusIcon

class SharingError(Exception):
	default_title = 'Sharing Error'
	default_content = 'An error occurred when uploading your screenshot.'
	def notify_error(self):
		try:
			title = self.args[1]
		except IndexError:
			title = self.default_title
		try:
			content = self.args[0]
		except IndexError:
			content = default_content
		StatusIcon().notify(title, content)
		return None
	pass

class AuthError(SharingError, ValueError):
	default_title = 'Authentication Error'
	default_content = 'An issue has occurred with authentication. Check your settings and try again.'
	pass

class ConnectionError(SharingError, EnvironmentError):
	default_title = 'Connection Error'
	default_content = '''
		Snappy could not connect to the server.
		This could be a problem with the server, or it could mean you aren't connected to the internet.
	'''
	pass

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
	module_name = configmanager['sharing.sharingservice']
	sharing_module = getattr(__import__('snappy.backend.httpstorage', fromlist=[module_name]), module_name)
	for key, value in sharing_module.__dict__.iteritems():
		if key.lower() == module_name.lower() + 'storage':
			return value(configmanager)
	raise NameError