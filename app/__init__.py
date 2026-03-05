from flask import Flask
from .api.books import api 
from .views.books import views

def create_app():

    app = Flask(__name__)
    
    app.register_blueprint(api)
    app.register_blueprint(views)

    return app