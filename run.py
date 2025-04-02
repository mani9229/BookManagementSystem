import os
from app import create_app
from app import db  
from app.config import get_config

#  Determine the environment
config_name = os.getenv('FLASK_ENV') or 'default'
app = create_app(get_config(config_name))

if __name__ == '__main__':
    #  Run the app
    app.run(debug=app.config['DEBUG'])


