from ftplib import FTP
from os.path import basename
from urllib import basejoin
from time import strftime
class FtpStorage:
	def __init__(self, configmanager):
		self.configmanager = configmanager
		self.server = configmanager.settings['ftpstorage.server']
		self.directory = configmanager.settings['ftpstorage.directory']
		self.httplocation = configmanager.settings['ftpstorage.httplocation']

	def store(self, filepath):
		username = self.configmanager.settings['ftpstorage.username']
		password = self.configmanager.get_password('ftpstorage.password')
		ftp = FTP(self.server, username, password)
		del password
		filename = strftime('%d-%b-%Y_%H-%M-%S.' + filepath.split('.')[-1])
		ftp.cwd(self.directory)
		f = open(filepath)
		ftp.storbinary('STOR %s' % filename, f)
		f.close()
		ftp.quit()
		ftp.close()
		return basejoin(self.httplocation, filename)