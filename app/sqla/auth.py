from typing import Optional

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

users = {
    "admin": {
        "name": "Admin",
        "avatar": "avatars/01.png",
        "roles": ["admin"],
    },
    "demo": {
        "name": "John Doe",
        "avatar": None,
        "roles": ["demo"],
    },
}


class MyAuthProvider(AuthProvider):
    """
    This is for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username in users and password == "graiadmin@3123":
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = users.get(request.session["username"])
            return True

        return False

    def get_admin_user(self, request: Request) -> Optional[AdminUser]:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            photo_url = request.url_for("statics", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
