FROM python:3.7-slim-buster

WORKDIR /src
COPY . .

RUN pip install -U poetry
RUN poetry install
# RUN poetry build
# RUN pip install dist/krypto-0.1.0-py3-none-any.whl

ENTRYPOINT [ "poetry" ]
CMD ["run", "krypto", "run", "."]