# FastAPI Exercise

This project serves as an exercise, showcasing the implementation of a web
application using the latest version of
[FastAPI](https://fastapi.tiangolo.com/). It incorporates essential tools such
as [Alembic](https://alembic.sqlalchemy.org/) for migrations and
[SQLModel](https://sqlmodel.tiangolo.com/) as the Object-Relational Mapping
(ORM), seamlessly integrated with [Pydantic V2](https://docs.pydantic.dev/2.5/)
and [SQLAlchemy V2.0](https://docs.sqlalchemy.org/en/20/).

## Getting Started

1. **Set Environment Variables:**

   Create an **.env** file in the `backend/app` folder and replicate the content
   from **.env.example**. Customize it based on your specific configuration.

2. **Run the Project:**

   Execute the following command to build and run the project:

   ```sh
   docker compose up -d --build
   ```

3. **Explore Swagger Docs:**

   Visit [http://localhost:8000/](http://localhost:8000/) to access the
   automatic interactive API documentation.

## Testing

Execute the following command to run tests:

```sh
scripts/dev.sh
```

## References

This project draws inspiration from the following resources:

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLModel Tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/)
- [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [Async configuration for FastAPI and SQLModel](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)
- [Minimal async FastAPI + PostgreSQL template](https://github.com/rafsaf/minimal-fastapi-postgres-template)

## To-Do List

- [x] Implement JWT authentication.
- [x] Create registration and password-reset email templates.
- [x] Implement validation for registration and password-reset via token.
- [x] Introduce BaseUUIDModel.
- [x] Implement Alembic migrations.
- [x] Integrate Celery for asynchronous email sending tasks.
- [x] Implement Asynchronous Database Management.
- [x] Implement async testing.
- [x] Implement Docker Compose.
- [x] Implement a sample one-to-many relationship.
- [ ] Establish a sample one-to-one relationship.
- [ ] Create a sample many-to-many relationship.
- [ ] Implement Pagination.
- [ ] Enable functionality to upload images and store them using Minio.
- [ ] Incorporate a sample React frontend.
