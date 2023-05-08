FROM python:latest

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt

RUN pip install connexion --upgrade

EXPOSE 9000
CMD ["python3",  "/code/app.py"]