FROM python:3.11.6

ARG USERNAME

ARG PROJECT_NAME=naivebayes

RUN useradd -m $USERNAME 

USER $USERNAME

WORKDIR /home/$USERNAME/$PROJECT_NAME

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . dev

CMD [ "python", "src/app.py" ]