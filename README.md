# Dynamic Flask Admin Panel

A beautiful, automatically configuring admin panel for Flask applications with SQLAlchemy models and PostgreSQL database integration.

## Features

- **Dynamic Model Discovery**: Automatically finds all your SQLAlchemy models
- **Beautiful Interface**: Modern Bootstrap 5 UI with responsive design
- **Enhanced Forms**: Automatically generates appropriate form fields based on model column types
- **Advanced Filtering**: Searchable and filterable data tables
- **Intuitive CRUD Operations**: Create, Read, Update, Delete operations for all your models
- **Flexible Configuration**: Easily customize via application configuration

## Project Structure

```
├── admin/                # Admin panel customization
│   ├── __init__.py       # Admin initialization and model discovery
│   ├── base.py           # Enhanced Admin Panel class
│   ├── forms.py          # Dynamic form generation
│   └── views.py          # Customized ModelView with enhancements
├── example/              # Example models
│   ├── __init__.py
│   └── models.py         # Example models for demonstration
├── static/               # Static assets
│   ├── css/
│   │   └── admin.css     # Custom admin styles
│   └── js/
│       └── admin.js      # Custom admin JavaScript
├── templates/            # HTML templates
│   └── admin/            # Admin interface templates
│       ├── model/        # Model specific templates
│       ├── index.html    # Admin dashboard
│       └── layout.html   # Base template
├── app.py                # Flask application setup
├── config.py             # Application configuration
├── main.py               # Entry point
└── models.py             # Your SQLAlchemy models
```

## Getting Started

1. Define your SQLAlchemy models in `models.py`
2. Configure your PostgreSQL database URL in environment variables
3. Run the application: `gunicorn --bind 0.0.0.0:5000 main:app`
4. Visit the admin panel at `/admin/`

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `SESSION_SECRET`: Secret key for Flask sessions (optional, defaults to a secure value)
- `FLASK_ADMIN_TITLE`: Custom title for the admin panel (optional)
- `ADMIN_MODEL_EXCLUDE`: List of model names to exclude from the admin panel (optional)

## Example Usage

Simply define your SQLAlchemy models:

```python
from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
```

The admin panel will automatically discover your models and create appropriate CRUD interfaces.

## Customization

You can customize the admin panel behavior by updating the configuration in `config.py` or by extending the `EnhancedModelView` class for specific models.

## Dependencies

- Flask
- Flask-Admin
- Flask-SQLAlchemy
- SQLAlchemy
- PostgreSQL
- WTForms
- Gunicorn

## License

MIT
