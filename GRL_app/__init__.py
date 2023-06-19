from .GRL_class import GRL_class

from flask import Flask
import datetime

from . import routes

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

## Calling GRL class 
player = GRL_class() 

routes.add_routes(app, player)