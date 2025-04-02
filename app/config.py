import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'JK_GEN_bookmanagement'
    #  Get from environment or provide a default
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_uri = os.environ.get('DATABASE_URL') or \
        'postgresql://neondb_owner:npg_d9JMeauYP4Oj@ep-damp-unit-a59836nl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require'  # using default for all

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://neondb_owner:npg_d9JMeauYP4Oj@ep-damp-unit-a59836nl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require' #  using default for all
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://neondb_owner:npg_d9JMeauYP4Oj@ep-damp-unit-a59836nl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require' #  using default for all
    

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name):
    """Returns the configuration object based on the environment."""
    return app_config.get(config_name, app_config['default'])