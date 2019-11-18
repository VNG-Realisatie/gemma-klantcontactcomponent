#!/bin/bash

set -u

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

JOB_NAME=push ./bin/release-docker-image.sh "$@"
