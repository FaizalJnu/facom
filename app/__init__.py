from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os

from config import config_by_name

mongo_client = None
user_collection = None

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    init_mongodb(app)
    

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

def init_mongodb(app):
    global mongo_client, user_collection
    
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client.get_database()
    user_collection = db.users