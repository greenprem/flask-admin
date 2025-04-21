from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy import func, select
import jinja2

from app.config import config
# from app.mongoengine import admin as admin_mongo
# from app.odmantic import admin as admin_odm
from app.sqla import admin as admin_sqla
from app.sqla import engine  # You'll need to import your engine
from app.sqla.models import Observation  # Import your Observation model

# Set up templates
templates = Jinja2Templates(directory="templates")

# String-based template for highest copy view
HIGHEST_COPY_TEMPLATE = """
{% extends "starlette_admin/base.html" %}

{% block content %}
<div class="container py-4">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title">Find Highest Copy Value</h5>
                </div>
                <div class="card-body">
                    <form method="post">
                        <div class="form-group mb-3">
                            <label for="client_name">Client Name</label>
                            <select id="client_name" name="client_name" class="form-control">
                                <option value="">-- Select Client --</option>
                                {% for client in clients %}
                                    <option value="{{ client }}">{{ client }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label for="site">Site</label>
                            <select id="site" name="site" class="form-control">
                                <option value="">-- Select Site --</option>
                                {% for site in sites %}
                                    <option value="{{ site }}">{{ site }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label for="greenhouse">Greenhouse</label>
                            <select id="greenhouse" name="greenhouse" class="form-control">
                                <option value="">-- Select Greenhouse --</option>
                                {% for greenhouse in greenhouses %}
                                    <option value="{{ greenhouse }}">{{ greenhouse }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label for="cycle_name">Cycle Name</label>
                            <select id="cycle_name" name="cycle_name" class="form-control">
                                <option value="">-- Select Cycle --</option>
                                {% for cycle in cycles %}
                                    <option value="{{ cycle }}">{{ cycle }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Find</button>
                    </form>
                    {% if highest_copy is not none %}
                        <div class="alert alert-success mt-3">
                            <h5>Result</h5>
                            <p>{{ result_message }}</p>
                        </div>
                    {% endif %}
                </div>
            </div>
            <div class="mt-3">
                <a href="/admin/observations" class="btn btn-secondary">Back to List</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

async def homepage(request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "config": config}
    )

async def highest_copy_view(request):
    # Get filter values
    highest_copy = None
    result_message = ""
    
    # Get options for select fields
    clients = []
    sites = []
    greenhouses = []
    cycles = []
    
    async with engine.connect() as conn:
        result = await conn.execute(select(Observation.client_name).distinct().order_by(Observation.client_name))
        clients = [c[0] for c in result if c[0]]
        
        result = await conn.execute(select(Observation.site).distinct().order_by(Observation.site))
        sites = [s[0] for s in result if s[0]]
        
        result = await conn.execute(select(Observation.greenhouse).distinct().order_by(Observation.greenhouse))
        greenhouses = [g[0] for g in result if g[0]]
        
        result = await conn.execute(select(Observation.cycle_name).distinct().order_by(Observation.cycle_name))
        cycles = [c[0] for c in result if c[0]]
    
    # If POST request, process the form
    if request.method == "POST":
        form_data = await request.form()
        client_name = form_data.get("client_name", "")
        site = form_data.get("site", "")
        greenhouse = form_data.get("greenhouse", "")
        cycle_name = form_data.get("cycle_name", "")
        
        # Build query with filters
        query = select(func.max(Observation.copy)).select_from(Observation)
        
        # Apply filters if provided
        filters_applied = False
        if client_name:
            query = query.filter(Observation.client_name == client_name)
            filters_applied = True
        if site:
            query = query.filter(Observation.site == site)
            filters_applied = True
        if greenhouse:
            query = query.filter(Observation.greenhouse == greenhouse)
            filters_applied = True
        if cycle_name:
            query = query.filter(Observation.cycle_name == cycle_name)
            filters_applied = True
            
        # Execute query
        async with engine.connect() as conn:
            result = await conn.execute(query)
            highest_copy = result.scalar()
        
        # Prepare message
        if filters_applied:
            filter_description = []
            if client_name:
                filter_description.append(f"Client: {client_name}")
            if site:
                filter_description.append(f"Site: {site}")
            if greenhouse:
                filter_description.append(f"Greenhouse: {greenhouse}")
            if cycle_name:
                filter_description.append(f"Cycle: {cycle_name}")
            
            filter_text = ", ".join(filter_description)
            result_message = f"Highest copy value for {filter_text}: {highest_copy}"
        else:
            result_message = f"Highest copy value overall: {highest_copy}"
    
    # Create a template environment
    env = jinja2.Environment(loader=jinja2.FunctionLoader(lambda name: HIGHEST_COPY_TEMPLATE if name == "highest_copy.html" else None))
    
    # Render the template string
    template = env.get_template("highest_copy.html")
    html_content = template.render({
        "request": request,
        "clients": clients,
        "sites": sites,
        "greenhouses": greenhouses,
        "cycles": cycles,
        "highest_copy": highest_copy,
        "result_message": result_message
    })
    
    # Return the rendered HTML
    return HTMLResponse(html_content)

# In your sqla/views.py file, update ObservationView
# from starlette.routing import Router
class CustomObservationView:
    @classmethod
    def extend_list_view(cls, request):
        """Injects a button into the list view"""
        return """
        <div class="mb-3">
            <a href="/admin/highest-copy" class="btn btn-primary">
                Find Highest Copy Value
            </a>
        </div>
        """

app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/admin/highest-copy", highest_copy_view, methods=["GET", "POST"]),
        Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
    ]
)
admin_sqla.mount_to(app)

# Add the button to the ObservationView
# You need to find a way to hook this into your ObservationView instance
# This will depend on how starlette_admin is implemented in your project
# Here's a general approach:
from app.sqla.views import ObservationView

# If starlette_admin allows you to modify templates or inject content
if hasattr(ObservationView, 'extend_list_template'):
    ObservationView.extend_list_template = CustomObservationView.extend_list_view