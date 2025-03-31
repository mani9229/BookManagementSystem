from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()  # Load environment variables

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_D9JMeauYP40j@ep-damp-unit-a59836n1-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app import api  # Import after app and db are defined
    app.register_blueprint(api.bp)

    return app
