# FastAPI Exercise

This project serves as an exercise showcasing the implementation of a web
application using [FastAPI](https://fastapi.tiangolo.com/),
[SQLModel](https://sqlmodel.tiangolo.com/) as the Object-Relational Mapping
(ORM) tool, which is compatible with
[Pydantic V2](https://docs.pydantic.dev/2.5/) and
[SQLAlchemy V2.0](https://docs.sqlalchemy.org/en/20/).

## References

This project draws inspiration from the following resources:

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLModel Tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/)
- [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [Async configuration for FastAPI and SQLModel ](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)
- [Minimal async FastAPI + PostgreSQL template](https://github.com/rafsaf/minimal-fastapi-postgres-template)

## To-Do List

- [x] Implement JWT authentication.
- [x] Create registration and password-reset email templates.
- [x] Implement validation for registration and password-reset via token.
- [x] Introduce BaseUUIDModel.
- [x] Implement Alembic migrations.
- [x] Integrate Celery for asynchronous email sending tasks.
- [x] Implement Asynchronous Database Management
- [x] Implement async testing.
- [ ] Implement docker compose
- [x] Implement a sample one-to-many relationship.
- [ ] Establish a sample one-to-one relationship.
- [ ] Create a sample many-to-many relationship.
- [ ] Implement Pagination.
- [ ] Enable functionality to upload images and store them using Minio.
- [ ] Incorporate a sample React frontend.
