# Project Title

A short description about the project and/or client.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The things you need before installing the software.

* Python with pip
* If you are planning to use a database, you will need to install the appropriate Python driver for that database and the database itself. For example, if you are using PostgreSQL, you will need to install the `psycopg2` package.
  * Change the configuration in `db/db_connection.py` to match your database settings.

### Installation

A step by step guide to get the development environment up and running.

1. Create a virtual environment with `python -m venv env`
2. Activate the virtual environment with `source env/bin/activate` on Linux or `env\Scripts\activate` on Windows
3. Install the dependencies with `pip install -r requirements.txt` or `pip install "fastapi[all]" sqlalchemy psycopg2 alembic bcrypt`
    * `"fastapi[all]"` is the FastAPI framework with all optional dependencies included.
    * `sqlalchemy` is the SQL toolkit and Object-Relational Mapping (ORM) library for Python.
    * `psycopg2` is the PostgreSQL adapter for the Python programming language.
    * `alembic` is a lightweight database migration tool for SQLAlchemy.
    * `bcrypt` is a hashing library for passwords.
4. Run the application with `python main.py`

## Usage

A few examples of useful commands and/or tasks.

```
$ First example
$ Second example
$ And keep this in mind
```

## Deployment

Additional notes on how to deploy this on a live or release system. Explaining the most important branches, what pipelines they trigger and how to update the database (if anything special).

### Server

* Live:
* Release:
* Development:

### Branches

* main: The main branch. It is always stable and contains the latest release.

## Additional Documentation and Acknowledgments

* Project folder on server:
* Confluence link:
* Asana board:
* etc...
