#Instalación y configuración Blacklist-app
FROM python:3.10 AS base
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV APP_PORT=5000
ENV DB_USER=postgres
ENV DB_PASSWORD=PgBlackList202314
ENV DB_HOST=pgblacklistdb.ca5xflkf2qn3.us-east-2.rds.amazonaws.com
ENV DB_PORT=5432
ENV DB_NAME=pgblacklistdb
RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip
WORKDIR /home/appuser/app
COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt
COPY src/. /home/appuser/app
EXPOSE 5000
CMD ["python", "application.py"]
#Instalación y configuración New Relic Agent
RUN pip install newrelic
ENV NEW_RELIC_APP_NAME=Blacklist
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_LOG_LEVEL=info
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=8f74f99bbb3dfafc764768aa48b080c1FFFFNRAL
ENTRYPOINT ["newrelic-admin", "run-program"]