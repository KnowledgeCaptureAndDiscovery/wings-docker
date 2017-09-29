#!/bin/bash

echo "export WINGS_MODE='dind'" > /usr/share/tomcat8/bin/setenv.sh
env | grep DOCKER | sed -e 's/^/export /' >> /usr/share/tomcat8/bin/setenv.sh
