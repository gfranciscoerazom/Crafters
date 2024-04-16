# region imports
from datetime import UTC, datetime, timedelta
from typing import Annotated
import bcrypt
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
# Import the APIRouter class to create a router
from fastapi.templating import Jinja2Templates
from db.db_connection import db_dependency
from db.schema import User
from sqlalchemy.orm import Session
from jose import jwt

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


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verifies if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (bytes): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticates a user by checking if the email and password match a user in the database.

    Args:
        db (Session): The database session.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        User: The user if the email and password match, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Creates an access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta): The expiration time of the token.

    Returns:
        str: The access token.
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        "Petierunt uti sibi concilium totius Galliae in diem certam indicere. Morbi fringilla convallis sapien, id pulvinar odio volutpat. A communi observantia non est recedendum.",
        algorithm="HS256"
    )
    return encoded_jwt


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


# region sign-up
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
        first_name (str): The first name of the user that comes from the form.
        last_name (str): The last name of the user that comes from the form.
        email (str): The email of the user that comes from the form.
        password (str): The password of the user that comes from the form.
        password_confirmation (str): The password confirmation of the user that comes from the form.

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

    token = create_access_token(
        {
            "id": new_user.id,
            "email": new_user.email,
        },
        timedelta(minutes=30)
    )

    response = RedirectResponse("/users/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
    # return RedirectResponse("/users/", status_code=status.HTTP_302_FOUND)


# region log-in
@router.get(
    "/log-in",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the log-in page.",
)
def log_in(request: Request):
    """
    Retrieve the log-in page.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered log-in.html template with the request object.
    """
    return templates.TemplateResponse("log-in.html", {
        "request": request,
    })


@router.post(
    "/log-in",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    description="Log-in a user.",
)
def log_in_user(request: Request, db: db_dependency, email: Annotated[str, Form(...)], password: Annotated[str, Form(...)]):
    """
    Log-in a user.

    Parameters:
        request (Request): The incoming request object.
        db (Session): The database session.
        email (str): The email of the user that comes from the form.
        password (str): The password of the user that comes from the form.

    Returns:
        TemplateResponse: The rendered log-in.html template with the request object.
    """
    user = authenticate_user(db, email, password)

    if not user:
        return templates.TemplateResponse("log-in.html", {
            "request": request,
            "message": "Invalid email or password.",
        })

    token = create_access_token(
        {
            "id": user.id,
            "email": user.email,
        },
        timedelta(minutes=30)
    )

    response = RedirectResponse("/users/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
