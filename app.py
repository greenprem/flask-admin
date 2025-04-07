import os
import importlib
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


# Create base class for SQLAlchemy models
class Base(declarative_base):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dynamic_admin_panel_secret_key")

# Configure database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Import config after initializing app
from config import configure_app
configure_app(app)

# Create all tables in the database
with app.app_context():
    # Import models
    try:
        import models
        logging.info("Found models.py in root directory")
    except ImportError:
        logging.warning("No models.py found in root directory")

    # Create database tables
    db.create_all()

    # Import and register admin interface
    from admin import init_admin
    init_admin(app, db)

    logging.info("Application initialized successfully")
