import urllib2
from urllib import urlencode
from snappy.backend.httpstorage import WebStorage, AuthError, ConnectionError, SharingError, post_multipart
from snappy.backend.configmanagers import get_conf_manager
from snappy.globals import PATHS
import xml.etree.cElementTree as ET
import pynotify
import gobject
import os
import time
import pango
configmanager = get_conf_manager
import gtk

class TwitPicStorage(WebStorage):
	nice_name = 'TwitPic online storage'
	defaults = {
		'twitpic.username': '',
		'twitpic.password': '',
		'twitpic.send_twitter': True
	}
	message = None
	def __init__(self, configmanager):
		self.configmanager = configmanager
		self.configmanager.set_post_upload_hook(self.twitter_post_send_hook)


	def store(self, filepath):
		TWITPIC_URL = 'http://twitpic.com/api/upload'
		username = self.configmanager.settings['twitpic.username']
		password = self.configmanager.get_password('twitpic.password')
		if not (username and password):
			raise AuthError('A username and/or password has not been entered.')
		f = open(filepath)
		try:
			image_data = f.read()
		finally:
			f.close()
		fields = {
			'username': username,
			'password': password,
		}
		result = post_multipart(TWITPIC_URL, fields.items(), [('media', filepath, image_data)]).read()
		print result
		tree = ET.XML(result)
		if tree.attrib.get('fail'):
			code = tree.find('err').attrib['code']
			message = tree.find('err').attrib['msg']
			if code == '1001':
				raise AuthError(message)
			else:
				raise SharingError(message, 'TwitPic Error')
		else:
			url = tree.findtext('mediaurl')
			return url



	def twitter_post(self, status):
		URL = 'https://twitter.com/statuses/update.xml'
		username = self.configmanager.settings['twitpic.username']
		password = self.configmanager.get_password('twitpic.password')
		if not (username and password):
			raise AuthError('A username and/or password has not been entered.')
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, URL, username, password)
		auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(auth_handler)
		try:
			result = opener.open(URL, urlencode({ 'status': status, }))
		except urllib2.HTTPError, e:
			if e.code == 401:
				raise AuthError('Username and password appear to be incorrect.')
			elif e.code == 502 or e.code == 500:
				raise ConnectionError('Twitter seems to be down right now, so your update wasn\'t posted.')
			elif e.code == 503:
				# wait 5 secs then try again until it works
				time.sleep(5)
				gobject.idle_add(self.twitter_post(status))
			else:
				print 'Error', e.code
				print e
				import pdb
				pdb.set_trace()
		except urllib2.URLError, e:
			raise ConnectionError(e.reason)
		else:
			return ('Updated Twitter Status', 'Snappy updated your twitter status.')
		return None


	def twitter_post_send_hook(self, url):
		def check_message(widget, buffer):
			widget.get_toplevel().hide()
			widget.emit('response')
		def update_chars(widget, event, label):
			try:
				label.old_colour
			except Exception:
				label.old_colour = label.style.text[gtk.STATE_NORMAL]
			chars_left = (140 - widget.get_buffer().get_end_iter().get_offset())
			if chars_left < 0:
				label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#EE0000'))
			else:
				label.modify_fg(gtk.STATE_NORMAL, label.old_colour)
			label.set_markup('<b>%s characters remaining</b>' % chars_left)
			if chars_left == 140 or chars_left < 0:
				widget.get_toplevel().set_response_sensitive(gtk.RESPONSE_OK, False)
			else:
				widget.get_toplevel().set_response_sensitive(gtk.RESPONSE_OK, True)

		# Set up the text buffer and select the text before the URL
		default_message = 'Just took a screenshot:'
		buffer = gtk.TextBuffer()
		anchor_tag = gtk.TextTag('anchor')
		anchor_tag.props.foreground = 'blue'
		anchor_tag.props.underline = pango.UNDERLINE_SINGLE
		buffer.get_tag_table().add(anchor_tag)
		buffer.set_text(default_message + ' ')
		# Add the URL in blue with underline
		buffer.insert_with_tags(buffer.get_end_iter(), url, anchor_tag)
		buffer.select_range(buffer.get_start_iter(), buffer.get_iter_at_offset(len(default_message)))

		send_button = gtk.Button('_Send')
		send_button.connect('clicked', check_message, buffer)

		dialog = gtk.Dialog(title='Post screenshot to Twitter', buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
		dialog.set_has_separator(False)

		# Set up TextView and ScrolledWindow
		view = gtk.TextView(buffer=buffer)
		view.set_wrap_mode(gtk.WRAP_WORD)
		viewport = gtk.ScrolledWindow()
		viewport.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		viewport.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		viewport.add(view)
		dialog.vbox.pack_start(viewport)

		# Add the label
		chars_left = (140 - buffer.get_end_iter().get_offset())
		label = gtk.Label('<b>%s characters left</b>' % chars_left)
		label.set_use_markup(True)
		view.connect('key-release-event', update_chars, label)
		dialog.set_size_request(420, 120)
		dialog.set_resizable(False)
		dialog.vbox.pack_start(label, expand=False)
		dialog.show_all()
		result = dialog.run()

		if result == gtk.RESPONSE_OK:
			# post to Twitter
			dialog.hide()
			try:
				twitter_result = self.twitter_post(buffer.props.text)
			except SharingError, e:
				e.notify_error()
			else:
				n = pynotify.Notification(twitter_result[0], twitter_result[1])
				n.show()
			dialog.destroy()

		return False

if __name__ == '__main__':
	TwitPicStorage.twitter_post_send_hook('http://awesome.url')