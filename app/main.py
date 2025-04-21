from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy import select, func
from app.db import SessionLocal
from app.sqla.models import Observation
from app.sqla.models import Client
#from app.sqla.models1 import Observation as Observation1
from app.config import config
from app.sqla import admin as admin_sqla
import json
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse, PlainTextResponse




# Login page
async def login_page(request):
    return HTMLResponse("""
        <html>
        <body>
            <form action="/login" method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
    """)

# Login handler
async def login_handler(request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if username == "admin" and password == "123456":
        request.session["user"] = "admin"
        return RedirectResponse("/", status_code=302)
    return PlainTextResponse("Invalid credentials", status_code=401)

# Protected homepage
async def homepage(request):
    if request.session.get("user") != "admin":
        return RedirectResponse("/login", status_code=302)
    return Jinja2Templates("templates").TemplateResponse(
        "index.html", {"request": request, "config": config}
    )


def panel(request):
    return Jinja2Templates("templates").TemplateResponse(
        "panel.html", {"request": request, "config": config}
    )

def greenhouse_panel(request):
    return Jinja2Templates("templates").TemplateResponse(
        "greenhouse_panel.html", {"request": request, "config": config}
    )


def get_max_copy(request: Request):
    # Extract parameters from the GET request
    client_name = request.query_params.get("client_name")
    site = request.query_params.get("site")
    greenhouse = request.query_params.get("greenhouse")
    cycle_name = request.query_params.get("cycle_name")

    if not all([client_name, site, greenhouse, cycle_name]):
        return JSONResponse({"error": "Missing required parameters"}, status_code=400)

    # Using a context manager for the session
    with SessionLocal() as db:
        stmt = (
            select(func.max(Observation.copy))
            .where(
                Observation.client_name == client_name,
                Observation.site == site,
                Observation.greenhouse == greenhouse,
                Observation.cycle_name == cycle_name,
            )
        )
        result = db.execute(stmt)
        max_copy = result.scalar()

    return JSONResponse({"max_copy": max_copy or 0})


# API: Return all client names
def get_clients(request: Request):
    with SessionLocal() as db:
        result = db.execute(select(Client.client_name))
        clients = [row[0] for row in result]
    return JSONResponse(clients)

# API: Get greenhouses for a client
def get_greenhouses(request: Request):
    client_name = request.query_params.get("client_name")
    if not client_name:
        return JSONResponse({"error": "Client name is required"}, status_code=400)

    with SessionLocal() as db:
        result = db.execute(select(Client).where(Client.client_name == client_name)).first()
        if not result:
            return JSONResponse({"error": "Client not found"}, status_code=404)
        client = result[0]
        return JSONResponse(client.greenhouse_name)

# API: Update greenhouses
async def update_greenhouses(request: Request):
    data = await request.json()
    client_name = data.get("client_name")
    greenhouses = data.get("greenhouses")

    if not client_name or not isinstance(greenhouses, dict):
        return JSONResponse({"error": "Invalid data"}, status_code=400)

    with SessionLocal() as db:
        stmt = select(Client).where(Client.client_name == client_name)
        result = db.execute(stmt).first()
        if not result:
            return JSONResponse({"error": "Client not found"}, status_code=404)

        client = result[0]
        client.greenhouse_name = greenhouses
        db.commit()

    return JSONResponse({"message": "Greenhouses updated successfully"})



app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/login", login_page, methods=["GET"]),
        Route("/login", login_handler, methods=["POST"]),
        Route("/panel", panel),
        Route("/greenhouse-panel", greenhouse_panel),
        Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
        Route("/get-max-copy", get_max_copy, methods=["GET"]),
        Route("/clients", get_clients, methods=["GET"]),
        Route("/get-greenhouses", get_greenhouses, methods=["GET"]),
        Route("/update-greenhouses", update_greenhouses, methods=["POST"]),

    ]
)

app.add_middleware(SessionMiddleware, secret_key="super-secret-key")


admin_sqla.mount_to(app)
