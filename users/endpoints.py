# region imports
from typing import Annotated
import bcrypt
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
# Import the APIRouter class to create a router
from fastapi.templating import Jinja2Templates
from db.db_connection import db_dependency
from db.schema import User

# region setup
# Create the router for the users
router = APIRouter(
    prefix="/users",  # Make that all the endpoints in this router start with /users
    tags=["users"],  # Add the tag "users" to all the endpoints in this router
)

# Create a template object to render the HTML files
templates = Jinja2Templates(directory="users/templates")

# region helper functions


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


# region endpoints
@router.get("/", response_class=HTMLResponse)
def read_users(request: Request):
    """
    Retrieve the index page.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered index.html template with the request object.
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@router.get(
    "/sign-up",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the sign-up page.",
)
def sign_up(request: Request):
    """
    Retrieve the sign-up page.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered sign-up.html template with the request object.
    """
    return templates.TemplateResponse("sign-up.html", {
        "request": request,
    })


@router.post(
    "/sign-up",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    description="Create a new user.",
)
def create_user(
    request: Request,
    db: db_dependency,
    first_name: Annotated[str, Form(...)],
    last_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    password_confirmation: Annotated[str, Form(...)],
):
    """
    Create a new user.

    Parameters:
        request (Request): The incoming request object.
        db (Session): The database session.

    Returns:
        TemplateResponse: The rendered sign-up.html template with the request object.
    """
    user = db.query(User).filter(User.email == email).first()

    if user:
        return templates.TemplateResponse("sign-up.html", {
            "request": request,
            "message": "The email is already registered.",
        })

    if password != password_confirmation:
        return templates.TemplateResponse("sign-up.html", {
            "request": request,
            "message": "The passwords do not match.",
        })

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(new_user)
    db.commit()

    return RedirectResponse("/users/", status_code=status.HTTP_302_FOUND)
