import win32api
try:
	import winxpgui as win_gui
except ImportError:
	import win32gui as win_gui
import win32con
import struct
import gtk
from snappy.ui.gtk.statusicon import SimpleGTKStatusIcon

class NotifyIconData(object):
	"""
	A Python version of the Win32 NID struct.
	From http://article.gmane.org/gmane.comp.python.general/541418
	"""
	_struct_format = (
		"I" # 		DWORD cbSize;
		"I" # 		HWND hWnd;
		"I" # 		UINT uID;
		"I" # 		UINT uFlags;
		"I" # 		UINT uCallbackMessage;
		"I" # 		HICON hIcon;
		"128s" #	TCHAR szTip[128];
		"I" # 		DWORD dwState;
		"I" # 		DWORD dwStateMask;
		"256s" # 	TCHAR szInfo[256];
		"I" #     	union {
			#    		UINT  uTimeout;
			#    		UINT  uVersion;
			#		} DUMMYUNIONNAME;
		"64s" #		TCHAR szInfoTitle[64];
		"I" #		DWORD dwInfoFlags;
		#			GUID guidItem;
	)
	_struct = struct.Struct(_struct_format)

	hWnd = 0
	uID = 0
	uFlags = 0
	uCallbackMessage = 0
	hIcon = 0
	szTip = ''
	dwState = 0
	dwStateMask = 0
	szInfo = ''
	uTimeoutOrVersion = 0
	szInfoTitle = ''
	dwInfoFlags = 0
	def pack(self):
		return self._struct.pack(
			self._struct.size,
			self.hWnd,
			self.uID,
			self.uFlags,
			self.uCallbackMessage,
			self.hIcon,
			self.szTip,
			self.dwState,
			self.dwStateMask,
			self.szInfo,
			self.uTimeoutOrVersion,
			self.szInfoTitle,
			self.dwInfoFlags)

def __setattr__(self, name, value):
	# avoid wrong field names
	if not hasattr(self, name):
		raise NameError, name
	self.__dict__[name] = value

class WinStatusIcon(SimpleGTKStatusIcon):
	def __init__(self):
		super(super(WinStatusIcon, self)).__init__()
		icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
		flags = win_gui.NIF_ICON | win_gui.NIF_MESSAGE | win_gui.NIF_TIP
		hicon = win_gui.LoadIcon(0, win32con.IDI_APPLICATION)
		nid = (0, 0, flags, win32con.WM_USER + 20, hicon, '')
		win_gui.Shell_NotifyIcon(nid, win_gui.NIM_ADD)
