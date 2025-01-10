from os import access
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import httpx
import uvicorn  # Library for serving the API
from fastapi import FastAPI  # Import the FastAPI class
# Import the engine for the database
from db.db_connection import SessionLocal, engine
import db.schema as schema  # Import the schema for the database
from db.schema import User  # Import the User class from the schema
from starlette.middleware.sessions import SessionMiddleware
from users.helpers.password_encryption import hash_password

# Import the endpoints for the users
from users import endpoints as users_endpoints
# Import the endpoints for the admin
from admin import endpoints as admin_endpoints
# Import the endpoints to compare careers
from compare_careers import endpoints as compare_careers_endpoints

app = FastAPI()  # Create an instance of the FastAPI class

# Create the tables in the database
schema.Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key="Morbi fringilla convallis sapien, id pulvinar odio volutpat. Hi omnes lingua, institutis, legibus inter se differunt. Non equidem invideo, miror magis posuere velit aliquet. Quid securi etiam tamquam eu fugiat nulla pariatur. Inmensae subtilitatis, obscuris et malesuada fames. Fictum, deserunt mollit anim laborum astutumque!",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the routers from the endpoints
app.include_router(users_endpoints.router)
app.include_router(admin_endpoints.router)
app.include_router(compare_careers_endpoints.router)


@app.get("/login-oauth")
def login_oauth():
    return RedirectResponse('https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=919034670843-dv2u5jdp82u75bllboooi9aekreuv4ej.apps.googleusercontent.com&response_type=code&redirect_uri=http://localhost:8000/login-code&scope=email%20profile%20openid&openid.realm', status_code=302)


@app.get("/login-code")
async def login_code(code: str):
    print(">>>>>>>>>>>>>>>>>.....", code)
    params = {
        'client_id': '919034670843-dv2u5jdp82u75bllboooi9aekreuv4ej.apps.googleusercontent.com',
        'client_secret': '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',
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/login-code'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://oauth2.googleapis.com/token", params=params, headers=headers)

    response_json = response.json()
    print(">>>>>>>>>>>>>>>>>>>>>>,,,,,,", response_json)
    access_token = response_json['access_token']
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
    return response.json()


db = SessionLocal()
admin_user = db.query(User).filter(User.first_name == "admin").first()

if admin_user is None:
    user = User(
        first_name="admin",
        last_name="admin",
        role="admin",
        email="admin@admin.admin",
        hashed_password=hash_password("admin")
    )
    db.add(user)
    db.commit()

db.close()

# Entry point for the API
if __name__ == "__main__":
    # Run the application using uvicorn and enable auto-reload
    uvicorn.run("main:app", reload=True)
