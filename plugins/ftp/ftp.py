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
from snappy.main.plugin import Plugin
from snappy.main.api import api
def ftpupload(plugin):
    print api.image.filename
def ftpgui(plugin, issettings):
    if issettings:
        #code to handle settings window goes here
        pass
    else:
        #code to handle window after preview goes here
        pass
    pass
ftp = Plugin(ftpupload, ftpgui)
ftp.setproperty('icon', 'ftp.png')
ftp.setproperty('fullname', 'FTP Uploader')
ftp.setproperty('description', 'Upload your screenshots to an FTP server.')
ftp.setproperty('settingsGUImethod', ftpgui)