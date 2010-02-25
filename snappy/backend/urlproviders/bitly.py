from snappy.backend.urlproviders import UrlProvider, AuthError
from urllib import urlencode
import urllib2
from BeautifulSoup import BeautifulSoup
try:
	import json
except ImportError:
	import simplejson as json
import cookielib
import socket

class BitlyUrlProvider(UrlProvider):
	nice_name = 'Bit.ly'
	api_url = 'http://api.bit.ly/shorten'
	defaults = {
		'sharing.shortener_username': '',
		'sharing.shortener_password': '',
		'bitly.api_key': 'R_39a6bde2bd0bf72d4f91d89e6e9f264f',
	}
	def shorten(self, url):
		socket.setdefaulttimeout(7.5)
		login = self.configmanager['sharing.shortener_username']
		use_anonymous = int(self.configmanager['sharing.shortener_anonymous'])
		publish_to_history = 1
		if use_anonymous or not login:
			login = 'snappy'
			publish_to_history = 0

		api_key = self.configmanager['bitly.api_key']
		data = urlencode([
			('version', '2.0.1'),
			('longUrl', url),
			('login', login),
			('apiKey', api_key),
			('history', publish_to_history)
		])
		f = urllib2.urlopen('http://api.bit.ly/shorten' + '?' + data)
		response = json.loads(f.read())
		f.close()
		print response
		if response['errorCode'] == 0:
			return response['results'].values()[0]['shortUrl']
		elif response['errorCode'] == 203:
			password = self.configmanager.get_password('sharing.shortener_password')
			try:
				possible_new_key = self.get_api_key_from_login(login, password)
			except AuthError:
				return super(BitlyUrlProvider, self).shorten(url)
			print possible_new_key
			if possible_new_key != api_key:
				# Looks like the user has reset their API key. Get a new one.
				self.configmanager['bitly.api_key'] = possible_new_key
				return self.shorten(url)
			else:
				# User has not reset their API key. Give up.
				return super(BitlyUrlProvider, self).shorten(url)
		else:
			return super(BitlyUrlProvider, self).shorten(url)

	@staticmethod
	def get_api_key_from_login(username, password):
		"""
		Get a user's API key from their username and password by manually
		logging in to bit.ly and scraping from /account/your_api_key.
		"""
		url = 'http://bit.ly/account/login?rd=%2Faccount%2Fyour_api_key'
		api_key_url = 'http://bit.ly/account/your_api_key'
		# Get the login page and parse to find the token.
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		urllib2.install_opener(opener)
		html = opener.open(url).read()
		soup = BeautifulSoup(html)
		form = soup.find('form')
		data = urlencode({
			'user': username,
			'password': password,
			'token': form.find('input', {'id': 'token'})['value'],
			'submitted': form.find('input', {'type': 'submit'})['value'],
		})
		# Send off the request to log in
		req = urllib2.Request(url, data, {'Referer': 'http://bit.ly/account/login?rd=%2Faccount%2Fyour_api_key'})
		auth_result = opener.open(req)
		auth_result.close()
		# We've got the cookies, now let's hop off to the API key page.
		req = urllib2.Request(api_key_url, headers={'Referer': 'http://bit.ly/account/login/?rd=%2Faccount%2Fyour_api_key'})
		result = opener.open(req).read()
		soup = BeautifulSoup(result)
		try:
			api_key = soup.find('input', {'name': 'bitly_api_key'})['value']
		except TypeError:
			raise AuthError('Bit.ly Login Error', 'Your login details are incorrect. Check they\'re correct and try again.')
		return api_key

if __name__ == '__main__':
	from snappy.backend.configmanagers import get_conf_manager
	b = BitlyUrlProvider(get_conf_manager())
	print b.shorten('http://google.com')