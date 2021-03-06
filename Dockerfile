FROM python:3.7.5-buster as production

MAINTAINER Keisuke Yamanaka <vaivailx@gmail.com>

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN echo "deb http://www.deb-multimedia.org buster main non-free" >> /etc/apt/sources.list \
    && apt-get update -oAcquire::AllowInsecureRepositories=true \
    && apt-get -y install deb-multimedia-keyring --allow-unauthenticated\
    && apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install ffmpeg \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

ENV APP_HOME /app
WORKDIR $APP_HOME
ADD ./Pipfile ./Pipfile.lock /app/

RUN pip --no-cache-dir install pipenv \
 && pipenv install --system --deploy \
 && pip uninstall -y pipenv virtualenv-clone virtualenv

ADD ./src /app

# Set Tokyo ID
ENV RADIKO_AREA_ID=JP13

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/radiko_recorder_account_key.json

ENV PORT '8080'
CMD python3 webapp.py
EXPOSE 8080

FROM production as test
RUN pip --no-cache-dir install pipenv \
 && pipenv install --system --deploy --dev \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
CMD python3 -m pytest
