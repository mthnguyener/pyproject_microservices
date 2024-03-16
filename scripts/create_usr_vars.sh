#!/bin/bash
# create_usr_vars.sh

help_function()
{
    echo ""
    echo "Create usr_vars configuration file."
    echo ""
    echo "Usage: $0"
    exit 1
}

# Parse arguments
while getopts "p:" opt
do
    case $opt in
        ? ) help_function ;;
    esac
done

# Create usr_vars configuration file
INITIAL_PORT=$(( (UID - 500) * 50 + 10000 ))
printf "%s\n" \
    "USER_NAME=${USER}" \
    "PROJECT_NAME=pyproject_microservices" \
    "NETWORK_NAME=pyproject_microservices-network" \
    "" \
    "# Data Directory" \
    "DATA_DIR=/mnt/data" \
    "" \
    "# Ports" \
    "PORT_APIGATEWAY=$INITIAL_PORT" \
    "PORT_DATAMANAGEMENT=$((INITIAL_PORT + 1))" \
    "PORT_FRONTEND=$((INITIAL_PORT + 2))" \
    "PORT_JUPYTER=$((INITIAL_PORT + 3))" \
    "PORT_MODELINFERENCE=$((INITIAL_PORT + 4))" \
    "PORT_MODELSERVING=$((INITIAL_PORT + 5))" \
    "PORT_MODELTRAINING=$((INITIAL_PORT + 6))" \
    "PORT_MONITORING=$((INITIAL_PORT + 7))" \
    "PORT_NGINX=$((INITIAL_PORT + 8))" \
    "PORT_PROFILE=$((INITIAL_PORT + 9))" \
    "" \
    > "usr_vars"
echo "Successfully created: usr_vars"

