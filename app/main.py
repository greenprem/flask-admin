from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy import func, select

from app.config import config
# from app.mongoengine import admin as admin_mongo
# from app.odmantic import admin as admin_odm
from app.sqla import admin as admin_sqla
from app.sqla import engine  # You'll need to import your engine
from app.sqla.models import Observation  # Import your Observation model

# Set up templates
templates = Jinja2Templates(directory="templates")

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
    
    # Render template
    return templates.TemplateResponse(
        "admin/highest_copy.html", 
        {
            "request": request,
            "clients": clients,
            "sites": sites,
            "greenhouses": greenhouses,
            "cycles": cycles,
            "highest_copy": highest_copy,
            "result_message": result_message
        }
    )

app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/admin/highest-copy", highest_copy_view, methods=["GET", "POST"], name="admin:highest_copy"),
        Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
    ]
)
admin_sqla.mount_to(app)