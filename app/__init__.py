# app.__init__.py

from flask import Flask

from app.api.helper import MongoJSONProvider
from .api.books import api 
from .views.books import views

def create_app():

    app = Flask(__name__)

    # This ensures ObjectId and Decimal128 are handled for ALL blueprints
    app.json = MongoJSONProvider(app)
    
    app.register_blueprint(api)
    app.register_blueprint(views)

    return app