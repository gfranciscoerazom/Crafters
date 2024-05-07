from fastapi.staticfiles import StaticFiles
import uvicorn  # Library for serving the API
from fastapi import FastAPI  # Import the FastAPI class
# Import the engine for the database
from db.db_connection import SessionLocal, engine
import db.schema as schema  # Import the schema for the database
from db.schema import User  # Import the User class from the schema
# Import the endpoints for the users
from users import endpoints as users_endpoints
# Import the endpoints for the admin
from admin import endpoints as admin_endpoints
from starlette.middleware.sessions import SessionMiddleware

from users.helpers.password_encryption import hash_password

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
