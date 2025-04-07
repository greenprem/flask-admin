import os
import importlib
import inspect
import logging
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import inspect as sql_inspect

from .base import AdminPanel
from .views import EnhancedModelView

def discover_models(db, models_module_name='models'):
    """Discover SQLAlchemy models from a given module"""
    models = []
    try:
        # Try to import the models module
        models_module = importlib.import_module(models_module_name)
        
        # Find all SQLAlchemy models in the module
        for attr_name in dir(models_module):
            attr = getattr(models_module, attr_name)
            
            # Check if it's a SQLAlchemy model class
            if inspect.isclass(attr) and hasattr(attr, '__tablename__'):
                # Skip abstract models
                if not hasattr(attr, '__abstract__') or not attr.__abstract__:
                    models.append(attr)
        
        logging.info(f"Discovered {len(models)} models from {models_module_name}")
    except ImportError:
        logging.warning(f"Could not import models from {models_module_name}")
    except Exception as e:
        logging.error(f"Error discovering models: {str(e)}")
    
    return models

def init_admin(app, db):
    """Initialize the admin interface with discovered models"""
    
    # Create Admin instance
    admin = AdminPanel(app, name=app.config.get('FLASK_ADMIN_TITLE', 'Flask Admin Panel'),
                      template_mode='bootstrap5')
    
    # List of models to exclude from admin
    exclude_models = app.config.get('ADMIN_MODEL_EXCLUDE', [])
    
    # Discover models from main models.py
    discovered_models = discover_models(db, app.config.get('ADMIN_MODELS_MODULE', 'models'))
    
    # Also check for models in example directory if it exists
    try:
        example_models = discover_models(db, 'example.models')
        discovered_models.extend(example_models)
    except Exception:
        pass
    
    # Register each model with the admin interface
    for model in discovered_models:
        model_name = model.__name__
        
        # Skip excluded models
        if model_name in exclude_models:
            logging.info(f"Skipping excluded model: {model_name}")
            continue
        
        # Create and register an enhanced view for this model
        view = EnhancedModelView(
            model, 
            db.session,
            name=model_name,
            category="Models"
        )
        
        admin.add_view(view)
        logging.info(f"Registered model in admin: {model_name}")
    
    return admin
