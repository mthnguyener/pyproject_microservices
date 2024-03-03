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
INITIAL_PORT=$(( (UID - 500) + 10000 ))
printf "%s\n" \
    "USER_NAME=${USER}" \
    "PROJECT_NAME=service_apigateway" \
    "NETWORK_NAME=pyproject_microservices-network" \
    "" \
    "# Data Directory" \
    "DATA_DIR=/mnt/data" \
    "" \
    "# Ports" \
    "PORT_APIGATEWAY=$INITIAL_PORT" \
    "" \
    > "usr_vars"
echo "Successfully created: usr_vars"

