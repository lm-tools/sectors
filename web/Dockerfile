FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD . /usr/src/app
RUN mkdir static
RUN pip install --no-cache-dir -r requirements.txt

RUN \
  apt-get update && \
  apt-get install -y ruby && \
  rm -rf /var/lib/apt/lists/*

RUN gem install bundler
RUN bundle install
