FROM python:3.11.6

ADD app.py .

WORKDIR /naive-bayes
COPY ./requirements.txt /naive-bayes/requirements.txt

RUN pip install -r requirements.txt

COPY . /naive-bayes

CMD [ "python", "./app.py" ]