#! /usr/bin/env sh

# Exit in case of error
set -e

docker compose -f docker-compose-test.yml config > docker-stack-test.yml

docker compose -f docker-stack-test.yml build
docker compose -f docker-stack-test.yml down --remove-orphans
docker compose -f docker-stack-test.yml up -d
docker compose -f docker-stack-test.yml exec -T backend bash /app/tests-start.sh "$@"
docker compose -f docker-stack-test.yml down -v --remove-orphans
