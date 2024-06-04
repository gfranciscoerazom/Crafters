from typing import Annotated
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.db_connection import db_dependency
from db.schema import Career, Faculty, UserCareer


router = APIRouter(
    prefix="/public/compare_careers",
    tags=["compare_careers"],
)

templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Get the compare careers page."
)
def get_compare_careers(request: Request, db: db_dependency):
    careers = db.query(Career).all()

    return templates.TemplateResponse(
        "/compare_careers/index.html",
        {
            "request": request,
            "careers": careers
        }
    )


@router.post(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Compare two careers."
)
def compare_careers(
    request: Request,
    db: db_dependency,
    career_id_1: Annotated[int, Form(...)],
    career_id_2: Annotated[int, Form(...)]
):
    career_1 = db.query(Career).filter(Career.id == career_id_1).first()
    career_2 = db.query(Career).filter(Career.id == career_id_2).first()

    faculty_1 = db.query(Faculty).filter(
        Faculty.id == career_1.faculty_id).first()
    faculty_2 = db.query(Faculty).filter(
        Faculty.id == career_2.faculty_id).first()

    pursuing_students_1 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_1, UserCareer.status == "cursando").count()
    pursuing_students_2 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_2, UserCareer.status == "cursando").count()

    graduated_students_1 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_1, UserCareer.status == "graduado").count()
    graduated_students_2 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_2, UserCareer.status == "graduado").count()

    expelled_students_1 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_1, UserCareer.status == "expulsado").count()
    expelled_students_2 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_2, UserCareer.status == "expulsado").count()

    resigned_students_1 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_1, UserCareer.status == "dimitido").count()
    resigned_students_2 = db.query(UserCareer).filter(
        UserCareer.career_id == career_id_2, UserCareer.status == "dimitido").count()

    comparison = {
        "name": (career_1.name, "", career_2.name),
        "Facultad": (faculty_1.name, "", faculty_2.name),
        "Descripción": (career_1.description, "", career_2.description),
        "Semestre": (career_1.semesters, career_1.semesters - career_2.semesters, career_2.semesters),
        "Créditos": (career_1.credits, career_1.credits - career_2.credits, career_2.credits),
        "Estudiantes cursando": (pursuing_students_1, pursuing_students_1 - pursuing_students_2, pursuing_students_2),
        "Estudiantes graduados": (graduated_students_1, graduated_students_1 - graduated_students_2, graduated_students_2),
        "Estudiantes expulsados": (expelled_students_1, expelled_students_1 - expelled_students_2, expelled_students_2),
        "Estudiantes dimitidos": (resigned_students_1, resigned_students_1 - resigned_students_2, resigned_students_2)
    }

    return templates.TemplateResponse(
        "/compare_careers/comparison.html",
        {
            "request": request,
            "comparison": comparison
        }
    )
