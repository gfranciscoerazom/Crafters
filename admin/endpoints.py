from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from users.helpers.jwt_token import user_dependency


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
