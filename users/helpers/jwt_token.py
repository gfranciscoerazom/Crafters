from datetime import UTC, datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jose import jwt

from db.schema import User, UserDict

SECRET_KEY = "Petierunt uti sibi concilium totius Galliae in diem certam indicere. Morbi fringilla convallis sapien, id pulvinar odio volutpat. A communi observantia non est recedendum."
ALGORITHM = "HS256"


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
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


# Revisar si usar TypedDict
# Ver si pone en una función el HTTPException
# Falta documentar
def get_user_information_from_token(request: Request) -> UserDict:
    token = request.cookies.get("access_token", None)

    if not token:
        request.session["error_message"] = "Please log in first."

        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,  # revisar el 306
            detail="Access token not found.",
            headers={"Location": "/users/log-in"},
        )

    try:
        payload: UserDict = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email = payload.get("email", None)
        id = payload.get("id", None)

        if not email or not id:
            request.session["error_message"] = "Invalid token."

            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail="Invalid token.",
                headers={"Location": "/users/log-in"},
            )

    except jwt.JWTError:
        request.session["error_message"] = "Invalid token."

        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Invalid token.",
            headers={"Location": "/users/log-in"},
        )

    del payload["exp"]

    return payload


def set_user_token_cookie(user: User, path: str):
    """
    Set the user token cookie and redirect the user.

    Parameters:
        user (User): The user object.
        path (str): The path to redirect the user.

    Returns:
        RedirectResponse: Redirects to the path with the token cookie.
    """
    token = create_access_token(
        user.to_UserDict(),
        timedelta(minutes=120)
    )

    response = RedirectResponse(path, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


user_dependency = Annotated[UserDict, Depends(get_user_information_from_token)]
