FROM python:3.7

ENV TOKEN_GITHUB = $TOKEN
ENV REPOINFO $GITHUB_REPOSITORY

RUN apt-get -y update && apt-get -y upgrade

RUN pip install poetry

COPY . .

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]