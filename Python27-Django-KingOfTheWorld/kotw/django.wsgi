import os, sys

sys.path.append('/home/ellis/cmpt470')
sys.path.append('/home/ellis/cmpt470/kotw')
os.environ['DJANGO_SETTINGS_MODULE']='settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
