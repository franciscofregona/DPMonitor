#!/usr/bin/python
import sys
#import logging
#logging.basicConfig(stream=sys.stderr)
#sys.path.insert(0,"/var/www/flask/dpmonitor")
sys.path.insert(0,"/var/www/flask/")

from dpmonitor import app as application

#application.secret_key = 'siliciosecular'