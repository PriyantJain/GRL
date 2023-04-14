from .GRL_class import GRL_class

from flask import Flask
import datetime

from . import routes

app = Flask(__name__)

## Calling GRL class 
player = GRL_class() 

routes.add_routes(app, player)