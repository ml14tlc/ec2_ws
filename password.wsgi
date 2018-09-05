import sys
# Add the folder to the Python path, so that the application can be found
sys.path.insert(0, '/var/www/rest')
# The WSGI module expects the application to be called "application"
from password import app as application
