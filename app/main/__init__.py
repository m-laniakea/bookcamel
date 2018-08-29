##
# Initialize main app from blueprint created in ../__init__.py create_app
##

from flask import Blueprint
main = Blueprint('main', __name__)

##
# "views" defines actions to take when a certain route is visited
#
# "errors" defines actions to take when errors are encountered
##
from . import views, errors, location_list 
