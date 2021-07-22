FROM python:3.7-slim-buster

WORKDIR /src
COPY . .

RUN pip install -U poetry
RUN poetry install

ENTRYPOINT [ "./entrypoint.sh" ]