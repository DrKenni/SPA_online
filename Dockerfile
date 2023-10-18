FROM python:3

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry init

COPY .  .

#CMD ["python", "manage.py", "runserver"]