# Crafters

Sitio web que permite a los estudiantes comparar diferentes programas académicos ofrecidos por la universidad además de una forma de comparar las habilidades que tiene el usuario con los estudiantes que han cursado el programa, que se han graduado, han sido expulsados y se retiraron de la carrera.

## Descripción

El proyecto “Crafters” es una plataforma web interactiva diseñada para estudiantes, personal académico y futuros candidatos interesados en los programas ofrecidos por la universidad. Esta herramienta permitirá a los usuarios comparar de manera eficiente y efectiva diversos aspectos de los programas académicos, como la duración, los requisitos de crédito, las tasas de graduación. Además de ayudarle al estudiante a escoger una carrera según sus habilidades. El objetivo es proporcionar una visión clara y concisa que ayude en la toma de decisiones informadas respecto a la elección de programas académicos.

## Explicación

El núcleo del proyecto se basa en una base de datos robusta que almacena información detallada sobre cada programa académico y las habilidades de los estudiantes. La interfaz de usuario será intuitiva, ofreciendo opciones de comparación tanto de carreras como de habilidades. Los usuarios podrán seleccionar programas para comparar y visualizar los datos en tablas comparativas. Y también podrán visualizar que tan bien se ajusta un programa a sus habilidades con respecto a las habilidades de otros estudiantes que cursaron, se graduaron, se retiraron o fueron expulsados de esa carrera.

## Alcance

El alcance principal del proyecto incluye:

* **Desarrollo de la Base de Datos**: Crear y mantener una base de datos actualizada con información de todos los programas académicos.
* **Interfaz de usuario**: Diseñar una interfaz amigable y accesible para todos los dispositivos.
* **Sistema de comparación de carreras**: Implementar un sistema que permita la comparación efectiva entre programas seleccionados por el usuario.
* **Sistema de Comparación de habilidades**: Implementar un sistema que permita comparar las habilidades de los estudiantes con las habilidades de los estudiantes que han cursado, se graduaron, se retiraron o fueron expulsados de un programa académico.

## Diagramas

### Diagrama Entidad Relación

<iframe width="560" height="315" src='https://dbdiagram.io/e/6615eb8703593b6b619dfd02/6627d01003593b6b61c2bc3d'> </iframe>

### Diagrama de Clases

![diagrama de clases](https://www.planttext.com/api/plantuml/png/XL71QiCm3BtxAqoEWnnwpQri37OPWx8FS6rr5NFY8IahO-pVPpTDh3QCtVpUa_IUP1yTitrb8Fjjh6qnT1O7AK_e7SRExeHmU2l4qV4HmajkE2KAMZaWiJox7ZIP9wyuIl4A8s-zu6VczYd5mdW29n2sqjc7_30_nlWbu-uTOvo2ZXa-rR1Sb1alFQfUBJReK5Vpxnt1V8aR0t-MjACu6NazHy_uopJZ0Em9FmJJe6c67bY0k1eJ19IA3ywFKRvMkpvE_B_Rdl-wsJIsRMrprzIxcdhXmXSvLrNfjcbQrAYxgRQBE0kRHRZ4DBy0)

### Diagrama de Casos de Uso

![diagrama de casos de uso](https://www.planttext.com/api/plantuml/png/XP512i8m44NtEKKlq2i8rGek2uBxRpB8GDf89jruUaCjQPj6NMRc_Pd_9z31-UeiOJIC8P32LEZ8YnjW6mr3FMitrqyO31i4fzGef25KdLp_X8Vll7juz92aaHrpmPrjr1jQUbUof3N7RMb4wjrOHbX-mRTnvw9fT9Zhn_XiwTDLIuoghWy_dNr1rmOpfEGpGtAxQdV62IkxBxExaUa7_aOia-k4Mw8KS4laPju0)

### Diagrama de Actividades

![diagrama de actividades](https://www.planttext.com/api/plantuml/png/pP112i9034NtFKMMxHNQXHHnARZn0EaajO7fH6R6XKVo75xCj1I4Mi6bcn32_-z_aZB6NDJdTCCe2ed1wuMnAQI7yf00QPImgo0F7A2ySweAWBfrJZHm0c8uSKmQq4Fha9wFKPmsffdyHoNfnM44mgopsYDqQ2csphSrsk0_kAO03YPRWlOwNZ6QmroH8svGrvAlY04xyK98l5LkI_P6iRUIPT2F9ot_RVwjxpnV)

### Wireframes

![diagrama de entidad relación](./imgs/New%20Wireframe%201.png)

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
3. Install the dependencies with `pip install -r requirements.txt` or `pip install "fastapi[all]" sqlalchemy psycopg2 alembic bcrypt "python-jose[cryptography]"`
    * `"fastapi[all]"` is the FastAPI framework with all optional dependencies included.
    * `sqlalchemy` is the SQL toolkit and Object-Relational Mapping (ORM) library for Python.
    * `psycopg2` is the PostgreSQL adapter for the Python programming language.
    * `alembic` is a lightweight database migration tool for SQLAlchemy.
    * `bcrypt` is a hashing library for passwords.
    * `"python-jose[cryptography]"` is a JavaScript Object Signing and Encryption library for Python.
4. Run the application with `python main.py`

<!-- ## Usage

A few examples of useful commands and/or tasks.

```bash
curl http://localhost:8000/users/log-in -X GET
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
* etc... -->