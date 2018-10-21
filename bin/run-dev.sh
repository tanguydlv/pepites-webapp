#!/bin/bash
PROJECT_NAME="pepites_webapp"

set -e

if [ ! $# -eq 1 ]
then
    echo "Usage: bin/run-dev.sh PORT"
    exit 1
fi

PORT=$1

docker build -t $PROJECT_NAME:develop .

docker build -t $PROJECT_NAME:devlocal - << EOF
FROM $PROJECT_NAME:develop
VOLUME /code
WORKDIR /code
EXPOSE $PORT
ENTRYPOINT flask db upgrade && python setup.py develop && flask run --host=0.0.0.0 --port=$PORT
EOF

echo "Docker service will listen on port: $PORT"

docker network create dev-net || true  # Automatically create dev network if it does not exist

docker run \
    --network dev-net \
    --name $PROJECT_NAME-db \
    --rm \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $PROJECT_NAME-db:/var/lib/postgresql/data/pgdata \
    -e POSTGRES_DB=database_dev \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -d postgres:10.2-alpine \
    || true  # do not fail if the container is already running

docker run \
    -p $PORT:$PORT \
    --network dev-net \
    --name $PROJECT_NAME-dev \
    --rm \
    -e DATABASE_URL=postgresql://user:password@$PROJECT_NAME-db/database_dev \
    -e FLASK_APP=pepites_webapp:app \
    -e FLASK_ENV=development \
    -e FLASK_SECRET_KEY=hax0r \
    -e API_URL=http://localhost:$PORT \
    `# Do not panic, the key below is the dev key and has limited access` \
    -e SENDGRID_API_KEY=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  \
    -e REDIRECT_SCHEME=http \
    -e SLACK_CHANNEL= \
    -e SLACK_URL= \
    -it \
    -v $PWD:/code \
    $PROJECT_NAME:devlocal

docker stop $PROJECT_NAME-db
