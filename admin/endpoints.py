from typing import Annotated
from fastapi import APIRouter, Form, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.db_connection import db_dependency
from db.schema import Career, Faculty, Skill, User, UserCareer, UserSkill
from users.helpers.jwt_token import user_dependency
from users.helpers.password_encryption import hash_password


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

templates = Jinja2Templates(directory="templates")


# region show all users
@router.get(
    "/show-users",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve all the users.",
)
def show_users(request: Request, user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    all_users: list[User] = db.query(User).all()

    return templates.TemplateResponse(
        "admin/users/show.html",
        {
            "request": request,
            "role": user["role"],
            "users": all_users,
        }
    )


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


# region create users
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

    first_name = first_name.strip()
    last_name = last_name.strip()

    if not first_name:
        return templates.TemplateResponse(
            "admin/users/create.html",
            {
                "request": request,
                "role": user["role"],
                "message": "The first name is required.",
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

    for skill_id in skill:
        db.add(UserSkill(user_id=new_user.id, skill_id=skill_id))

    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


# region delete users
@router.get(
    "/delete-user/{user_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Delete a user.",
)
def delete_user(request: Request, user: user_dependency, db: db_dependency, user_id: int):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return RedirectResponse("/admin/show-users", status_code=status.HTTP_303_SEE_OTHER)

    db.delete(db_user)
    db.commit()

    return RedirectResponse("/admin/show-users", status_code=status.HTTP_303_SEE_OTHER)


# region add a user to a career
@router.get(
    "/add-user-to-career",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to add a user to a career.",
)
def add_user_to_career(request: Request, user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    all_users: list[User] = db.query(User).all()
    all_careers: list[Career] = db.query(Career).all()

    return templates.TemplateResponse(
        "admin/users/add_to_career.html",
        {
            "request": request,
            "role": user["role"],
            "users": all_users,
            "careers": all_careers,
        }
    )


@router.post(
    "/add-user-to-career",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Add a user to a career.",
)
def add_user_to_career_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    user_id: Annotated[int, Form(...)],
    career_id: Annotated[int, Form(...)],
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    db.add(UserCareer(user_id=user_id, career_id=career_id, status="pursuing"))
    db.commit()

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "role": user["role"],
        }
    )


# region user details
@router.get(
    "/user-details/{user_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the details of a user.",
)
def user_details(request: Request, user: user_dependency, db: db_dependency, user_id: int):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return RedirectResponse("/admin/show-users", status_code=status.HTTP_303_SEE_OTHER)

    user_skills = db.query(UserSkill, Skill).join(
        Skill).filter(UserSkill.user_id == user_id).all()
    user_careers = db.query(UserCareer, Career).join(
        Career).filter(UserCareer.user_id == user_id).all()

    return templates.TemplateResponse(
        "admin/users/details.html",
        {
            "request": request,
            "role": user["role"],
            "user": db_user,
            "skills": user_skills,
            "careers": user_careers,
        }
    )


# region edit users
@router.get(
    "/edit-user/{user_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the page to edit a user.",
)
def edit_user(request: Request, user: user_dependency, db: db_dependency, user_id: int):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return RedirectResponse("/admin/show-users", status_code=status.HTTP_303_SEE_OTHER)

    all_skills: list[Skill] = db.query(Skill).all()
    user_skills: list[UserSkill] = db.query(UserSkill).filter(
        UserSkill.user_id == user_id).all()
    user_skills = [skill.skill_id for skill in user_skills]
    user_careers = db.query(UserCareer, Career).join(
        Career).filter(UserCareer.user_id == user_id).all()

    return templates.TemplateResponse(
        "admin/users/edit.html",
        {
            "request": request,
            "role": user["role"],
            "user": db_user,
            "skills": all_skills,
            "user_skills": user_skills,
            "user_careers": user_careers,
        }
    )


@router.post(
    "/edit-user/{user_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Edit a user.",
)
def edit_user_post(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    user_id: int,
    first_name: Annotated[str, Form(...)],
    last_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    role: Annotated[str, Form(...)],
    skill: Annotated[list, Form(...)],
    career_id: Annotated[list[int], Form(...)],
    career_status: Annotated[list, Form(...)],
    is_active: Annotated[bool, Form(...)] = False,
):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return RedirectResponse("/admin/show-users", status_code=status.HTTP_303_SEE_OTHER)

    # Valida que el email tenga un formato válido
    if "@" not in email or " " in email or email.count("@") > 1 or email.split("@")[1].count(".") == 0:
        return templates.TemplateResponse(
            "admin/users/edit.html",
            {
                "request": request,
                "role": user["role"],
                "user": db_user,
                "message": "The email is not valid.",
            }
        )

    db_user.first_name = first_name
    db_user.last_name = last_name
    db_user.email = email
    db_user.role = role
    db_user.is_active = is_active

    db.commit()

    db.query(UserSkill).filter(UserSkill.user_id == user_id).delete()

    for skill_id in skill:
        db.add(UserSkill(user_id=user_id, skill_id=skill_id))

    db.commit()

    db.query(UserCareer).filter(UserCareer.user_id == user_id).delete()
    users_careers: list[UserCareer] = [
        UserCareer(
            user_id=user_id,
            career_id=career_id,
            status=status
        ) for career_id, status in zip(career_id, career_status)
    ]
    db.add_all(users_careers)
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


# region show all careers
@router.get(
    "/show-careers",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve all the careers.",
)
def show_careers(request: Request, user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

    all_careers: list[Career, Faculty] = db.query(
        Career, Faculty).join(Faculty).all()

    return templates.TemplateResponse(
        "admin/careers/show.html",
        {
            "request": request,
            "role": user["role"],
            "careers": all_careers,
        }
    )
