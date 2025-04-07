import logging
from flask import flash, request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.helpers import get_redirect_target
from flask_admin.babel import gettext
from wtforms.validators import ValidationError
from sqlalchemy import func, or_, and_, desc, asc

from .forms import get_enhanced_form

class EnhancedModelView(ModelView):
    """
    Enhanced ModelView with better styling, filtering, and usability features
    """
    
    # UI customization
    can_view_details = True
    details_modal = True
    edit_modal = True
    create_modal = True
    can_export = True
    
    # Template customization
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    details_template = 'admin/model/details.html'
    
    # Pagination
    page_size = 25
    
    # Search and filter configuration
    column_searchable_list = []
    column_filters = []
    named_filter_urls = True
    
    # UI Enhancement
    column_display_pk = True
    column_display_actions = True
    
    def __init__(self, model, session, **kwargs):
        # Initialize empty lists before super init to prevent auto-detection issues
        self.column_searchable_list = []
        self.column_filters = []
        
        # Automatically determine searchable columns (string types)
        for col in model.__table__.columns:
            col_type = str(col.type)
            # Add string-like columns to searchable list
            if 'CHAR' in col_type or 'VARCHAR' in col_type or 'TEXT' in col_type:
                self.column_searchable_list.append(col.name)
            
            # Add all columns to filters
            self.column_filters.append(col.name)
        
        # Call super init after setting up the lists
        super(EnhancedModelView, self).__init__(model, session, **kwargs)
    
    def scaffold_form(self):
        """
        Create an enhanced form for the model
        """
        return get_enhanced_form(self.model, self.session)
    
    def get_query(self):
        """
        Enhanced query method with better sorting
        """
        query = super(EnhancedModelView, self).get_query()
        
        # Handle global search
        search_query = request.args.get('search', '')
        if search_query and self.column_searchable_list:
            search_terms = [term.strip() for term in search_query.split() if term.strip()]
            
            if search_terms:
                search_conditions = []
                for term in search_terms:
                    term_conditions = []
                    for column_name in self.column_searchable_list:
                        try:
                            column = getattr(self.model, column_name)
                            term_conditions.append(column.ilike(f'%{term}%'))
                        except AttributeError:
                            continue
                    
                    if term_conditions:
                        search_conditions.append(or_(*term_conditions))
                
                if search_conditions:
                    query = query.filter(and_(*search_conditions))
        
        return query
    
    def is_accessible(self):
        """Always accessible for now, could be extended with auth"""
        return True
    
    def handle_view_exception(self, exc):
        """Handle exceptions in views with user-friendly messages"""
        if isinstance(exc, ValidationError):
            flash(f'Validation error: {str(exc)}', 'error')
            return True
            
        flash(f'An error occurred: {str(exc)}', 'error')
        logging.exception(exc)
        return super().handle_view_exception(exc)
