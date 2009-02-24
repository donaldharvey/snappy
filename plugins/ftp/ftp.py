#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from snappy.main.plugin import Plugin
from snappy.main.api import api
def ftpupload(plugin):
    print api.image.filename
ftp = Plugin(ftpupload)
ftp.setproperty('icon', 'flickr.png')
ftp.setproperty('fullname', 'Flickr Uploader')
ftp.setproperty('description', 'Upload your screenshots to flickr.')