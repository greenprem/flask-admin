from flask_admin import Admin, expose
from flask_admin.base import AdminIndexView
from flask import render_template

class CustomAdminIndexView(AdminIndexView):
    """Custom admin index view with enhanced template"""
    
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class AdminPanel(Admin):
    """Enhanced Admin class with additional features"""
    
    def __init__(self, app=None, name=None, url=None, subdomain=None,
                 index_view=None, translations_path=None, endpoint=None,
                 static_url_path=None, base_template=None,
                 template_mode=None, category_icon_classes=None):
        
        if index_view is None:
            index_view = CustomAdminIndexView()
            
        super().__init__(
            app, name, url, subdomain, index_view, translations_path,
            endpoint, static_url_path, base_template, template_mode, 
            category_icon_classes
        )
