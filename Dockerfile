FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "8001"]