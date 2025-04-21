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

def get_max_copy(request: Request):
    # Use request.body() for synchronous JSON parsing
    body = request.body()
    print(body)
    data = json.loads(body)

    client_name = data.get("client_name")
    site = data.get("site")
    greenhouse = data.get("greenhouse")
    cycle_name = data.get("cycle_name")

    # Synchronous database session handling
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
