import os
import __builtin__
class AuthError(ValueError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

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

# Following utility methods are slightly modified from http://code.activestate.com/recipes/146306/.
def post_multipart(url, fields, files):
	"""
	Post fields and files to an http host as multipart/form-data.
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return the server's response page.
	"""
	import httplib
	import urlparse
	urlparts = urlparse.urlsplit(url)
	host, selector = urlparts[1], urlparts[2]
	content_type, body = _encode_multipart_formdata(fields, files)
	h = httplib.HTTP(host)
	h.putrequest('POST', selector)
	h.putheader('content-type', content_type)
	h.putheader('content-length', str(len(body)))
	h.endheaders()
	h.send(body)
	errcode, errmsg, headers = h.getreply()
	return h.file.read()

def _encode_multipart_formdata(cls, fields, files):
	"""
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return (content_type, body) ready for httplib.HTTP instance
	"""
	BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
	CRLF = '\r\n'
	L = []
	print fields
	for (key, value) in fields:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % str(key))
		L.append('')
		L.append(str(value))
	for (key, filename, value) in files:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(filename)))
		mimetype = guess_type(filename)[0] or 'application/octet-stream'
		L.append('Content-Type: %s' % mimetype)
		L.append('')
		L.append(str(value))
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join(L)
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	return content_type, body
