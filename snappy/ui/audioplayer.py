import os
import platform
if platform.system == 'Windows':
	import winsound
else:
	import gst

class AudioPlayer(object):
	def __init__(self, path_to_file=''):
		if os.path.isfile(path_to_file):
			self.file = os.path.abspath(path_to_file)
		if platform.system != 'Windows':
			self._player = gst.element_factory_make('playbin', 'player')
			self._player.props.uri = 'file://' + self.file
			bus = self._player.get_bus()
			bus.add_signal_watch()
			bus.connect('message', self._gst_player_message)

	def _gst_player_message(self, bus, message):
		if message.type == gst.MESSAGE_EOS:
			self._player.set_state(gst.STATE_NULL)
		elif message.type == gst.MESSAGE_ERROR:
			self._player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "gStreamer Error: %s" % err, debug

	def play(self):
		if platform.system != 'Windows':
			self._player.set_state(gst.STATE_PLAYING)
		else:
			winsound.PlaySound(self.file, winsound.SND_ASYNC | winsound.SND_FILENAME)
