#!/bin/bash

NAME='wings'

if [ $# -gt 0 ]; then
    NAME=$1
fi

PORT=8080
ARGS='--volume /var/run/docker.sock:/var/run/docker.sock'

echo "# --------------------------------------------"
echo "# WINGS Server will be started on port ${PORT}"
echo "# ARGS: ${ARGS}"
echo "# --------------------------------------------"

docker inspect --type container ${NAME} > /dev/null 2>&1

# If a container with ${NAME} already exists, start it.
if [ $? -eq 0 ]; then
    docker start ${NAME}
    docker exec --interactive \
                --tty \
                ${NAME} /bin/bash
else
    docker volume create --name "${NAME}_vol" > /dev/null
    docker run --interactive \
               --tty \
               --env WINGS_MODE='dind' \
               --volume "${NAME}_vol":/opt/wings \
               --name ${NAME} \
               --publish 8080:8080 \
               ${ARGS} kcapd/wings-base
fi
