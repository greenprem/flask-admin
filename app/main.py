from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy import select, func
from app.db import SessionLocal
from app.sqla.models import Observation
from app.config import config
from app.sqla import admin as admin_sqla
import json


def homepage(request):
    return Jinja2Templates("templates").TemplateResponse(
        "index.html", {"request": request, "config": config}
    )

def panel(request):
    return Jinja2Templates("templates").TemplateResponse(
        "panel.html", {"request": request, "config": config}
    )

def get_max_copy(request: Request):  # No longer async
    # Extract parameters from the GET request
    client_name = request.query_params.get("client_name")
    site = request.query_params.get("site")
    greenhouse = request.query_params.get("greenhouse")
    cycle_name = request.query_params.get("cycle_name")

    if not all([client_name, site, greenhouse, cycle_name]):
        return JSONResponse({"error": "Missing required parameters"}, status_code=400)

    # Use synchronous session here since it's a GET request (non-async)
    with SessionLocal() as session:
        stmt = (
            select(func.max(Observation.copy))
            .where(
                Observation.client_name == client_name,
                Observation.site == site,
                Observation.greenhouse == greenhouse,
                Observation.cycle_name == cycle_name,
            )
        )
        result = session.execute(stmt)
        max_copy = result.scalar()

    return JSONResponse({"max_copy": max_copy or 0})

app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/panel", panel),
        Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
        Route("/get-max-copy", get_max_copy, methods=["POST"]),
    ]
)

admin_sqla.mount_to(app)
