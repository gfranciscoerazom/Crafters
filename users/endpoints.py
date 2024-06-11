# region imports
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
# Import the APIRouter class to create a router
from fastapi.templating import Jinja2Templates
from db.db_connection import db_dependency
from db.schema import Career, Skill, User, UserCareer, UserSkill
from users.helpers.authenticate_user import authenticate_user
from users.helpers.jwt_token import set_user_token_cookie, user_dependency
from users.helpers.password_encryption import hash_password
from sqlalchemy import desc, func

# region setup
# Create the router for the users
router = APIRouter(
    prefix="/users",  # Make that all the endpoints in this router start with /users
    tags=["users"],  # Add the tag "users" to all the endpoints in this router
)

# Create a template object to render the HTML files
templates = Jinja2Templates(directory="templates")


# region endpoints
@router.get("/", response_class=HTMLResponse)
def read_users(
    request: Request,
    user: user_dependency
):
    """
    Retrieve the index page.

    Parameters:
        request (Request): The incoming request object.
        user (dict): The user of the session.

    Returns:
        TemplateResponse: The rendered index.html template with the request object.
    """
    return templates.TemplateResponse("users/index.html", {
        "request": request,
        "role": user["role"],
    })


# region sign-up
@router.get(
    "/sign-up",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the sign-up page.",
)
def sign_up(request: Request, db: db_dependency):
    """
    Retrieve the sign-up page.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered sign-up.html template with the request object.
    """
    all_skills: list[Skill] = db.query(Skill).all()

    return templates.TemplateResponse(
        "users/sign-up.html",
        {
            "request": request,
            "skills": all_skills,
        }
    )


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
    skill: Annotated[list, Form(...)],
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
        request.session["error_message"] = "The email is already registered try to log in."
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/users/log-in"},
        )

    if password != password_confirmation:
        return templates.TemplateResponse("users/sign-up.html", {
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

    for skill_id in skill:
        db.add(UserSkill(user_id=new_user.id, skill_id=skill_id))

    db.commit()

    return set_user_token_cookie(new_user, "/users/")


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
    message = request.session.get("error_message", None)

    if message:
        del request.session["error_message"]

    return templates.TemplateResponse("users/log-in.html", {
        "request": request,
        "message": message,
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
        return templates.TemplateResponse("users/log-in.html", {
            "request": request,
            "message": "Invalid email or password.",
        })

    return set_user_token_cookie(user, "/users/")


# region log-out
@router.get(
    "/log-out",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    description="Log-out a user.",
)
def log_out():
    """
    Log-out a user.

    Returns:
        RedirectResponse: Redirects to the log-in page.
    """
    response = RedirectResponse(
        "/users/log-in",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("access_token")
    return response


# region compare skills
@router.get(
    "/compare-skills",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retrieve the compare skills page.",
)
def compare_skills(request: Request, user: user_dependency, db: db_dependency):
    """
    Retrieve the compare skills page.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered compare-skills.html template with the request object.
    """
    user_skills = db.query(Skill).join(UserSkill).filter(
        UserSkill.user_id == user["id"]).all()

    all_careers = db.query(Career).all()

    return templates.TemplateResponse(
        "users/compare-skills.html",
        {
            "request": request,
            "user_skills": user_skills,
            "user": user,
            "careers": all_careers,
        }
    )


def get_element(list, index):
    try:
        return list[index]
    except IndexError:
        return 0


def balance_skills(skills_of_students):
    balanced_skills_of_students = []
    for i in range(10):
        skill = get_element(skills_of_students, i)

        if skill == 0:
            break

        skill = list(skill)

        if i < 5:
            skill[2] *= 5 - i
        balanced_skills_of_students.append(skill)
    return balanced_skills_of_students


@router.post(
    "/compare-skills",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Compare two skills.",
)
def compare_skills(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    career_id: Annotated[int, Form(...)],
):
    user_skills = db.query(Skill).join(UserSkill).filter(
        UserSkill.user_id == user["id"]).all()

    all_careers = db.query(Career).all()

    skills_of_pursuing_students = db.query(
        Skill.id,
        Skill.name,
        func.count(Skill.id).label("count")
    ).join(UserSkill).join(User).join(UserCareer).filter(
        UserCareer.career_id == career_id, UserCareer.status == "cursando").group_by(Skill.id).order_by(desc("count")).all()

    skills_of_graduated_students = db.query(
        Skill.id,
        Skill.name,
        func.count(Skill.id).label("count")
    ).join(UserSkill).join(User).join(UserCareer).filter(
        UserCareer.career_id == career_id, UserCareer.status == "graduado").group_by(Skill.id).order_by(desc("count")).all()

    skills_of_expelled_students = db.query(
        Skill.id,
        Skill.name,
        func.count(Skill.id).label("count")
    ).join(UserSkill).join(User).join(UserCareer).filter(
        UserCareer.career_id == career_id, UserCareer.status == "expulsado").group_by(Skill.id).order_by(desc("count")).all()

    skills_of_resigned_students = db.query(
        Skill.id,
        Skill.name,
        func.count(Skill.id).label("count")
    ).join(UserSkill).join(User).join(UserCareer).filter(
        UserCareer.career_id == career_id, UserCareer.status == "dimitido").group_by(Skill.id).order_by(desc("count")).all()

    # Balance de importancia de las habilidades
    balanced_skills_of_pursuing_students = balance_skills(
        skills_of_pursuing_students)

    balanced_skills_of_graduated_students = balance_skills(
        skills_of_graduated_students)

    balanced_skills_of_expelled_students = balance_skills(
        skills_of_expelled_students)

    balanced_skills_of_resigned_students = balance_skills(
        skills_of_resigned_students)

    sum_of_pursuing_students = sum(
        [skill[2] for skill in balanced_skills_of_pursuing_students])

    sum_of_graduated_students = sum(
        [skill[2] for skill in balanced_skills_of_graduated_students])

    sum_of_expelled_students = sum(
        [skill[2] for skill in balanced_skills_of_expelled_students])

    sum_of_resigned_students = sum(
        [skill[2] for skill in balanced_skills_of_resigned_students])

    user_id_skills = [skill.id for skill in user_skills]

    pursuing_user_skills = [
        skill for skill in balanced_skills_of_pursuing_students if skill[0] in user_id_skills]

    graduated_user_skills = [
        skill for skill in balanced_skills_of_graduated_students if skill[0] in user_id_skills]

    expelled_user_skills = [
        skill for skill in balanced_skills_of_expelled_students if skill[0] in user_id_skills]

    resigned_user_skills = [
        skill for skill in balanced_skills_of_resigned_students if skill[0] in user_id_skills]

    sum_of_pursuing_user_skills = sum(
        [skill[2] for skill in pursuing_user_skills])

    sum_of_graduated_user_skills = sum(
        [skill[2] for skill in graduated_user_skills])

    sum_of_expelled_user_skills = sum(
        [skill[2] for skill in expelled_user_skills])

    sum_of_resigned_user_skills = sum(
        [skill[2] for skill in resigned_user_skills])

    percentage_of_pursuing_user_skills = round(
        (sum_of_pursuing_user_skills / sum_of_pursuing_students) * 100, 2)

    percentage_of_graduated_user_skills = round(
        (sum_of_graduated_user_skills / sum_of_graduated_students) * 100, 2)

    percentage_of_expelled_user_skills = round(
        (sum_of_expelled_user_skills / sum_of_expelled_students) * 100, 2)

    percentage_of_resigned_user_skills = round(
        (sum_of_resigned_user_skills / sum_of_resigned_students) * 100, 2)

    return templates.TemplateResponse(
        "users/compare-skills.html",
        {
            "request": request,
            "user_skills": user_skills,
            "user": user,
            "careers": all_careers,
            "skills_of_pursuing_students": skills_of_pursuing_students,
            "skills_of_graduated_students": skills_of_graduated_students,
            "skills_of_expelled_students": skills_of_expelled_students,
            "skills_of_resigned_students": skills_of_resigned_students,
            "percentage_of_pursuing_user_skills": percentage_of_pursuing_user_skills,
            "percentage_of_graduated_user_skills": percentage_of_graduated_user_skills,
            "percentage_of_expelled_user_skills": percentage_of_expelled_user_skills,
            "percentage_of_resigned_user_skills": percentage_of_resigned_user_skills,
        }
    )
