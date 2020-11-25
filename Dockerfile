FROM python:3.8.5

ADD . /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]