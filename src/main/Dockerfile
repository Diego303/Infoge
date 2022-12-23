FROM python:3.7
# ADVERTENCIA: ES NECESARIO TENER EL FICHERO KEYS.CONF PARA COMPILAR EL DOCKER
RUN mkdir /micro
WORKDIR /micro
ADD . /micro
RUN pip install -r requirements.txt

EXPOSE 5000 8080
CMD ["python", "/micro/infoge_app.py"]