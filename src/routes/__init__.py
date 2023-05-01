from flask import Blueprint

routes = Blueprint("routes", __name__)

from .download import *
from .index import *
from .youtube import *
