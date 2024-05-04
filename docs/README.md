# Crafters

Sitio web que permite a los estudiantes comparar diferentes programas académicos ofrecidos por la universidad.

## Descripción

El proyecto “Crafters” es una plataforma web interactiva diseñada para estudiantes, personal académico y futuros candidatos interesados en los programas ofrecidos por la universidad. Esta herramienta permitirá a los usuarios comparar de manera eficiente y efectiva diversos aspectos de los programas académicos, como la duración, los requisitos de crédito, las tasas de graduación y las oportunidades laborales posteriores a la graduación. El objetivo es proporcionar una visión clara y concisa que ayude en la toma de decisiones informadas respecto a la elección de programas académicos.

## Explicación

El núcleo del proyecto se basa en una base de datos robusta que almacena información detallada sobre cada programa académico. La interfaz de usuario será intuitiva, ofreciendo filtros y opciones de comparación personalizables. Los usuarios podrán seleccionar programas para comparar y visualizar los datos en tablas comparativas dinámicas.

## Alcance

El alcance principal del proyecto incluye:

* **Desarrollo de la Base de Datos**: Crear y mantener una base de datos actualizada con información de todos los programas académicos.
* **Interfaz de Usuario**: Diseñar una interfaz amigable y accesible para todos los dispositivos.
* **Sistema de Comparación**: Implementar un sistema que permita la comparación efectiva entre programas seleccionados por el usuario.
* **Feedback de Usuarios**: Incorporar un mecanismo para que los usuarios puedan dejar comentarios y valoraciones sobre los programas.

## Diagramas

### Diagrama Entidad Relación

#### Entidades Principales

1. **Programa Académico**
   * Atributos: ID del programa, nombre, descripción, duración, créditos necesarios, departamento.
2. **Departamento**
   * Atributos: ID del departamento, nombre del departamento, director, contacto.
3. **Curso**
   * Atributos: ID del curso, nombre del curso, descripción, créditos, ID del programa.
4. **Estudiante**
   * Atributos: ID del estudiante, nombre, apellido, ID del programa, año de ingreso.
5. **Profesor**
   * Atributos: ID del profesor, nombre, apellido, especialidad, ID del departamento.

#### Relaciones

* **Programa Académico** - **Departamento**: Un departamento puede ofrecer varios programas académicos.
* **Programa Académico** - **Curso**: Un programa académico incluye varios cursos.
* **Curso** - **Profesor**: Un profesor puede enseñar varios cursos.
* **Estudiante** - **Programa Académico**: Un estudiante está inscrito en un programa académico.
* **Estudiante** - **Curso**: Un estudiante toma varios cursos.

#### Gráfico

<iframe width="560" height="315" src='https://dbdiagram.io/e/6615eb8703593b6b619dfd02/6627d01003593b6b61c2bc3d'> </iframe>

### Diagrama de Clases

![diagrama de clases](https://www.planttext.com/api/plantuml/svg/fLJBQiCm4BpxAtHCAVc1K4fBMagWX5Bw0njfOnPahRihvT3IVwyisubDA7tThD5eLhCxrer6a9WQNraFgkP9k1PeuDQ2muOic_VAcAKXjp8KOlaEtEm4LqQZKAWBv52jK6k9mnnF0Zqu7hQ2ZYBh5Yqg2B6EUvU6Tn43oYRiMPfoRd4naRiq5hnD7kG55FH1mAKZQ-yPUfK32kt9WZpZQoBjYct2yNeTTyViguzgi7o7RMu1D1ZYJzsIe8qiCz1oY93HsOM_TGHATG39RT-ZiYpQuMDbHYZp3qoki3rruredKTPEw36lhyho-kIdhFytjd58VnXDldQJ3_CQV9b2HqMTJsWGEvg-EBazsRZNc1n1YFWpBz2Yz-Hu3WRYJQWbI__1otfemvgRrcC4rtTzr3a6xTvZJJlArS7DKpbFscZo7uPGMxG4fTJlaZRDpcr9dJiFKOcaZIaNUCk-9iKMqyhRX0SOrSU0PfldhyToUJtxmRwWbFBLPEGTU4Qj-cWFUtrURZ2uxldw1000)

### Diagrama de Casos de Uso

![diagrama de casos de uso](https://www.planttext.com/api/plantuml/svg/TP9BJWCn38RtEOMNxQ8SW0LgW17g0ZIYWhsLk4FKFAh4WtY8Go6Eq8lX6QQZqiSo_dxzl-ruNXWpjy4hJoi6Jf1Tyy9WNIR3BaLLrYvkC6E03PerDhJaTq_GOOoD9wNGSCfG5MwjmyW4MA0QgZNbaY9wRT1IS2PriDO3rJQuw0fdjF8IefKQZM4fX0BUfD3b6sccpgcHJh2CTWK-5K05inbChjjYK29tegcGuo9SNC5ayFnNlmGNZMyjZOOdL2DxfWotnEWz5R3aHqsVUfxsySladN6oULZ4LSf1Xjl-nAu5UcEATamv8rGYg7Mlq8PRzExZG7BKqaw-_KRvMtXewJMT4bJUoP_ipTo7_R4xAjr927mgBMQN-dqSCcqCbNtqI4E3zzrrHF6do6cgljHSPkrkxnS0)

### Diagrama de Actividades

![diagrama de actividades](https://www.planttext.com/api/plantuml/svg/dL0x3i8m3Drp2c-KApG32DI13L69FQGkM4gToacu5LCFW4GlHWfKCBDPxsUzjmxHI4oTKwz3gNB7PCa8r1Xe75YhiaQ7rfBdZ2wslkkDv6il_YocCs6X5RLGFEuLMyzHnW7wcLij8LwGeGZZRQa0oihXcUGh00FsawWd_eWo0_Rz7br0ADY_x9iKhFcnwpypkQ4sTwtuEbKDtkNECJNG812tNhfPMHxGqYcd2uO-OHv9vwLyhzOvOvhj2G00)

### Wireframes

![diagrama de entidad relación](./docs/imgs/New%20Wireframe%201.png)

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