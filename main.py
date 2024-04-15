from fastapi.staticfiles import StaticFiles
import uvicorn  # Library for serving the API
from fastapi import FastAPI  # Import the FastAPI class
from db.db_connection import engine  # Import the engine for the database
import db.schema as schema  # Import the schema for the database
from users import endpoints  # Import the endpoints for the users

app = FastAPI()  # Create an instance of the FastAPI class

# Create the tables in the database
schema.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the routers from the endpoints
app.include_router(endpoints.router)

# Entry point for the API
if __name__ == "__main__":
    # Run the application using uvicorn and enable auto-reload
    uvicorn.run("main:app", reload=True)
