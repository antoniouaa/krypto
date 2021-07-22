FROM python:3.7-slim-buster

RUN pip install -U poetry && poetry install

WORKDIR /src
COPY . .

RUN poetry build
RUN pip install dist/krypto-0.1.0-py3-none-any.whl

RUN chmod +x /src/entrypoint.sh

CMD /src/entrypoint.sh