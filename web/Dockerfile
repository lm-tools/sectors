FROM python:3.5-onbuild
RUN \
  apt-get update && \
  apt-get install -y ruby && \
  rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements/production.txt

RUN gem install bundler
RUN bundle install
