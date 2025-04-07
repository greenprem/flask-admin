import os

def configure_app(app):
    """Configure Flask application with settings"""
    
    # Admin panel title and basic configuration
    app.config['FLASK_ADMIN_TITLE'] = os.environ.get('ADMIN_TITLE', 'Flask Admin Panel')
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    
    # Custom configuration options for our admin panel
    app.config['ADMIN_MODEL_EXCLUDE'] = os.environ.get('ADMIN_MODEL_EXCLUDE', '').split(',')
    app.config['ADMIN_MODELS_MODULE'] = os.environ.get('ADMIN_MODELS_MODULE', 'models')
    
    # Row items per page in list view
    app.config['ADMIN_ROWS_PER_PAGE'] = int(os.environ.get('ADMIN_ROWS_PER_PAGE', 25))
    
    # Enable CSV export
    app.config['ADMIN_ENABLE_EXPORT'] = os.environ.get('ADMIN_ENABLE_EXPORT', 'true').lower() == 'true'

    return app
