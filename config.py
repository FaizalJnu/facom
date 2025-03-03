import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_db')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/test_db')

class ProductionConfig(Config):
    DEBUG = False

# Dictionary to map configuration based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}