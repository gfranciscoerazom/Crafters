from fastapi.staticfiles import StaticFiles
import uvicorn  # Library for serving the API
from fastapi import FastAPI  # Import the FastAPI class
from db.db_connection import engine  # Import the engine for the database
import db.schema as schema  # Import the schema for the database
from users import endpoints  # Import the endpoints for the users
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()  # Create an instance of the FastAPI class

# Create the tables in the database
schema.Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key="Morbi fringilla convallis sapien, id pulvinar odio volutpat. Hi omnes lingua, institutis, legibus inter se differunt. Non equidem invideo, miror magis posuere velit aliquet. Quid securi etiam tamquam eu fugiat nulla pariatur. Inmensae subtilitatis, obscuris et malesuada fames. Fictum, deserunt mollit anim laborum astutumque!",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the routers from the endpoints
app.include_router(endpoints.router)

# Entry point for the API
if __name__ == "__main__":
    # Run the application using uvicorn and enable auto-reload
    uvicorn.run("main:app", reload=True)
