FROM python:3.8-alpine

# Inicializar variables de entorno
ENV SECRETKEY = ""
ENV DEBUG = True
ENV NAMEDB = ""
ENV USERDB = ""
ENV PASSWORDDB = ""
ENV HOSTDB = ""
ENV PORTDB = ""

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN apk add --update --no--cache --virtual .tmp gcc libc-dev
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 8088

ENTRYPOINT python manage.py runserver 0.0.0.0:8088

# Instrucciones:
    # Ejecutar docker build -t finanzas-desarrollo .
    # Rellenar con los datos de tu entorno y ejecutar: Docker run –p 30000:8088 –e SECRETKEY= -e DEBUG=True –e NAMEDB="finanzas-diplomado-desarrollo" -e PASSDB="myPass" -e HOSTDB="192.168.100.133" -e PORTDB="8088" --name nombreImagenEjemplo seguido del nombre de imagen con la que deseo trabajar