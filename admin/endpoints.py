from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.db_connection import db_dependency
from db.schema import User
from users.helpers.jwt_token import user_dependency
from users.helpers.password_encryption import hash_password


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def welcome_admin(
    request: Request,
    user: user_dependency
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


@router.get(
    "/create-user",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to create a new user.",
)
def create_user(request: Request, user: user_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/users/create.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


@router.post(
    "/create-user",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Create a new user.",
)
def create_user_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    first_name: Annotated[str, Form(...)],
    last_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    password_confirmation: Annotated[str, Form(...)],
    role: Annotated[str, Form(...)],
):
    print(f"{user=}")
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    # Valida que el email tenga un formato válido
    if "@" not in email or " " in email or email.count("@") > 1 or email.split("@")[1].count(".") == 0:
        return templates.TemplateResponse(
            "admin/users/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The email is not valid.",
            }
        )

    db_user = db.query(User).filter(User.email == email).first()

    if db_user:
        return templates.TemplateResponse(
            "admin/users/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The email is already registered.",
            }
        )

    if password != password_confirmation:
        return templates.TemplateResponse(
            "admin/users/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The passwords do not match.",
            }
        )

    if not role:
        return templates.TemplateResponse(
            "admin/users/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The role is required.",
            }
        )

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )

    db.add(new_user)
    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )
