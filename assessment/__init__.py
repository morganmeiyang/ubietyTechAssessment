from flask import Flask

from assessment.extensions import db
from assessment.routes import main

def create_app(database_uri = 'sqlite:///database.db'):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        db.init_app(app)
        app.register_blueprint(main)
        return app