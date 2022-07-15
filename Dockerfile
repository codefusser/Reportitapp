# build a django project with docker container

FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /Reportitapp
COPY requirements.txt /Reportitapp/
RUN pip install -r requirements.txt
COPY . /Reportitapp