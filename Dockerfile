FROM python:3.7

ENV TOKEN_GITHUB = $TOKEN_GITHUB
ENV REPOINFO $GITHUB_REPOSITORY

RUN apt-get -y update && apt-get -y upgrade

RUN pip install poetry

COPY . .

LABEL "maintainer"="antoniouaa <antoniouaa@hotmail.com>"
LABEL "com.github.actions.name"="Krypto"
LABEL "com.github.actions.description"="Programmatically generate GitHub Issues from comments in code"
LABEL "com.github.actions.icon"="alert-icon"
LABEL "com.github.actions.color"="blue"

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]