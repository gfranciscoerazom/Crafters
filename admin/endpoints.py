from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.db_connection import db_dependency
from db.schema import Career, Faculty, Skill, User
from users.helpers.jwt_token import user_dependency
from users.helpers.password_encryption import hash_password


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

templates = Jinja2Templates(directory="templates")


# region create users
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
def create_user(request: Request, user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    all_skills: list[Skill] = db.query(Skill).all()

    return templates.TemplateResponse(
        "admin/users/create.html",
        {
            "request": request,
            "role": user["role"],
            "skills": all_skills,
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
    skill: Annotated[list, Form(...)],
):
    print(f"{skill=}")

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


# region create skills
@router.get(
    "/create-skill",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to create a new skill.",
)
def create_skill(request: Request, user: user_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/skills/create.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


@router.post(
    "/create-skill",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Create a new skill.",
)
def create_skill_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    name: Annotated[str, Form(...)],
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    name = name.strip()

    if not name:
        return templates.TemplateResponse(
            "admin/skills/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The name is required.",
            }
        )

    new_skill = Skill(name=name)

    db.add(new_skill)
    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


# region create faculty
@router.get(
    "/create-faculty",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to create a new faculty.",
)
def create_faculty(request: Request, user: user_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/faculties/create.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


@router.post(
    "/create-faculty",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Create a new faculty.",
)
def create_faculty_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    name: Annotated[str, Form(...)],
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    name = name.strip()

    if not name:
        return templates.TemplateResponse(
            "admin/faculties/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The name is required.",
            }
        )

    new_faculty = Faculty(name=name)

    db.add(new_faculty)
    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


# region create career
@router.get(
    "/create-career",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to create a new career.",
)
def create_career(request: Request, user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    all_faculties: list[Faculty] = db.query(Faculty).all()

    return templates.TemplateResponse(
        "admin/careers/create.html",
        {
            "request": request,
            "role": user["role"],
            "faculties": all_faculties,
        }
    )


# class Career(Base):
#     """
#     Represents a career that a user can take.

#     Attributes:
#         id (int): The unique identifier for the career.
#         name (str): The name of the career.
#         description (str): The description of the career.
#         semesters (int): The number of semesters of the career.
#         credits (int): The number of credits of the career.
#         faculty_id (int): The unique identifier for the faculty.
#     """

#     __tablename__ = 'careers'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String)
#     semesters = Column(Integer)
#     credits = Column(Integer)
#     faculty_id = Column(Integer, ForeignKey('faculties.id'))
@router.post(
    "/create-career",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Create a new career.",
)
def create_career_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    name: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    semesters: Annotated[int, Form(...)],
    credits: Annotated[int, Form(...)],
    faculty_id: Annotated[int, Form(...)],
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    name = name.strip()
    description = description.strip()

    if not name:
        return templates.TemplateResponse(
            "admin/careers/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The name is required.",
            }
        )

    if not description:
        return templates.TemplateResponse(
            "admin/careers/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The description is required.",
            }
        )

    if semesters < 1:
        return templates.TemplateResponse(
            "admin/careers/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The number of semesters must be greater than 0.",
            }
        )

    if credits < 1:
        return templates.TemplateResponse(
            "admin/careers/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The number of credits must be greater than 0.",
            }
        )

    new_career = Career(
        name=name,
        description=description,
        semesters=semesters,
        credits=credits,
        faculty_id=faculty_id,
    )

    db.add(new_career)
    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )
