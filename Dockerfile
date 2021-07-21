FROM python:3.8-slim-buster

WORKDIR /krypto
COPY . /krypto/

RUN pip install -U poetry && poetry install

RUN poetry build
RUN pip install dist/krypto-0.1.0-py3-none-any.whl

ENTRYPOINT ["/entrypoint.sh"]