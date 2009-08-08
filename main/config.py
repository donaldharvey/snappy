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

import ConfigParser, os

gconfset = True
enabledplugins = ['ftp', 'flickr']
config = ConfigParser.ConfigParser() #change to gconf later
print os.getcwd()
config.readfp(open(os.path.join(os.path.dirname(__file__), 'config.cfg')))
urlprovider = 'tr.im'
try:
	urlusername = config.get('urlprovider', 'username')
	urlpassword = config.get('urlprovider', 'password')
except Exception:
	urlusername = ''
	urlpassword = ''


