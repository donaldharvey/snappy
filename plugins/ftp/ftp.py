#!/usr/bin/env python
# Copyright (C) 2009 Donald S. F. Harvey
#
# This file is part of Snappy.
#
# Snappy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snappy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snappy.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
<<<<<<< HEAD:plugins/ftp/ftp.py
from snappy.main.plugin import Plugin
from snappy.main.api import api
def ftpupload(plugin):
    print api.image.path
def ftpgui(plugin, issettings):
=======
sys.path.append('../..')
from snappy.main.plugin import Plugin
from snappy.main import api
from threading import Thread, Lock
from time import sleep
import pynotify
def ftpupload(plugin):
    settings = plugin.settings
    if settings['server'] and settings['username'] and settings['password']:
        from ftplib import FTP, error_perm
        from urllib import quote
        try:
            pynotify.init('message-summary-body')
            n = pynotify.Notification('Uploading to FTP started.')
            n.show()
            f = FTP(settings['server'])
            f.login(settings['username'], settings['password'])
            
            if settings['directory']:
                f.cwd(settings['directory'])
            f.storbinary("STOR " + api.api.image.filename, file(api.api.image.path, 'rb'))
            f.quit()
            
        except error_perm:
            print 'Permission error'
            return False
        except Exception:
            print 'Other error'
            return False
        else:
            n = pynotify.Notification('Upload complete')
            n.show()
            return settings['baseurl'] + '/' + quote(api.api.image.filename)
            
            
def ftpgui(plugin, issettings=False):
>>>>>>> 89c7e19... Added working tr.im-ing.:plugins/ftp/ftp.py
    if issettings:
        #code to handle settings window goes here
        pass
    else:
        #code to handle window after preview goes here
        pass
    pass
ftp = Plugin(ftpupload, ftpgui)
<<<<<<< HEAD:plugins/ftp/ftp.py
ftp.setproperty('icon', 'ftp.png')
ftp.setproperty('fullname', 'FTP Uploader')
ftp.setproperty('description', 'Upload your screenshots to an FTP server.')
ftp.setproperty('settingsGUImethod', ftpgui)
=======
ftp.settings = {
    'server': '9milesmedia.com',
    'directory': 'screenshots',
    'port': None,
    'username': '', #TODO: get from conf file
    'password': '', #TODO: get from conf file
    'baseurl': 'http://donaldharvey.co.uk/screenshots',
    'addtoclipboard': True
}
ftp.setproperty('icon', 'ftp.png')
ftp.setproperty('fullname', 'FTP Uploader')
ftp.setproperty('description', 'Upload your screenshots to an FTP server.')
ftp.setproperty('settingsGUImethod', ftpgui)
    
>>>>>>> 89c7e19... Added working tr.im-ing.:plugins/ftp/ftp.py
