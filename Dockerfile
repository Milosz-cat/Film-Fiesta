FROM python:3.10-slim

WORKDIR /app/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECIDE 1

COPY requirements.txt requirements.txt

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc wget curl unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
