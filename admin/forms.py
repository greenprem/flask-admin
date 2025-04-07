from wtforms import Form, StringField, TextAreaField, BooleanField, IntegerField
from wtforms import FloatField, DateField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from wtforms.widgets import TextArea

def get_enhanced_form(model, session):
    """
    Dynamically create a form for the model with enhanced field handling
    """
    # Get model table columns
    columns = model.__table__.columns
    
    # Create form class dictionary
    form_attrs = {}
    
    # Process each column to create appropriate form fields
    for column in columns:
        field_name = column.name
        field_args = {
            'label': field_name.replace('_', ' ').title(),
            'validators': []
        }
        
        # Add validators based on column properties
        if not column.nullable and not column.primary_key and not column.server_default:
            field_args['validators'].append(DataRequired())
        else:
            field_args['validators'].append(Optional())
        
        # Handle character length for string fields
        if hasattr(column.type, 'length') and column.type.length:
            field_args['validators'].append(Length(max=column.type.length))
        
        # Add placeholder attribute
        field_args['render_kw'] = {'placeholder': field_args['label']}
        
        # Determine field type based on SQLAlchemy column type
        col_type = str(column.type)
        
        # Skip primary key columns that are auto-generated
        if column.primary_key and column.autoincrement:
            continue
            
        # Create the appropriate field based on column type
        if 'INTEGER' in col_type:
            form_attrs[field_name] = IntegerField(**field_args)
        elif 'FLOAT' in col_type or 'NUMERIC' in col_type or 'DECIMAL' in col_type:
            form_attrs[field_name] = FloatField(**field_args)
        elif 'BOOLEAN' in col_type:
            form_attrs[field_name] = BooleanField(field_args['label'])
        elif 'DATE' in col_type and 'TIME' in col_type:
            form_attrs[field_name] = DateTimeField(**field_args)
        elif 'DATE' in col_type:
            form_attrs[field_name] = DateField(**field_args)
        elif 'TEXT' in col_type:
            field_args['render_kw']['rows'] = 5
            form_attrs[field_name] = TextAreaField(**field_args)
        else:
            # Default to StringField for others (VARCHAR, CHAR, etc.)
            form_attrs[field_name] = StringField(**field_args)
        
        # Special handling for fields that seem to be for specific data types
        if 'email' in field_name.lower():
            field_args['validators'].append(Email())
            
    # Create and return the form class
    return type(f'{model.__name__}Form', (Form,), form_attrs)
