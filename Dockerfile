# build env
FROM node:13.12.0-alpine as build
WORKDIR /app

# install git
RUN apk update && apk upgrade && \
    apk add --no-cache git

COPY ./client /app/
RUN yarn install --ignore-engines
RUN yarn build

# production env
# use alpine linux with standard python-3.9
FROM python:3.9-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git

# install gcc and g++
RUN set -ex && \
    apk add --no-cache gcc musl-dev g++

# open up port 80
EXPOSE 8000

# set working directory
WORKDIR /app

# copy files over
COPY db /app/db/
COPY githubify /app/githubify/
COPY requirements.txt /app/requirements.txt
COPY clock.py /app/clock.py
COPY app.py /app/app.py
COPY .env /app/.env

# copy build over
COPY --from=build /app/build /app/client/build

# install python dependencies
RUN pip install -r requirements.txt

# spin up server
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
