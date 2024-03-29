#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <service> <ports>"
    exit 1
fi

# Get service name from command-line argument
SERVICE=$1
TOOL=$2

# Define the appropriate port line based on the selected service
case $SERVICE in
    api_gateway)
        PORT_LINE="\${PORT_APIGATEWAY}:\${PORT_APIGATEWAY}"
        ;;
    front_end)
        PORT_LINE="\${PORT_FRONTEND}:\${PORT_FRONTEND}"
        ;;
    model_serving)
        PORT_LINE="\${PORT_MODELSERVING}:\${PORT_MODELSERVING}"
        ;;
    *)
        echo "Invalid service"
        exit 1
        ;;
esac

# Define the appropriate port line based on the selected service
case $TOOL in
    PROFILE)
        sed -i "/\${PORT_PROFILE}:\${PORT_PROFILE}/d" ./docker/docker-compose.yaml
        PORT_TOOL="\${PORT_PROFILE}:\${PORT_PROFILE}"
        sed -i "/^ *- ${PORT_LINE}/a \ \ \ \ - \${PORT_PROFILE}:\${PORT_PROFILE}" ./docker/docker-compose.yaml
        ;;
    JUPYTER)
        sed -i "/\${PORT_JUPYTER}:\${PORT_JUPYTER}/d" ./docker/docker-compose.yaml
        PORT_TOOL="\${PORT_JUPYTER}:\${PORT_JUPYTER}"
        sed -i "/^ *- ${PORT_LINE}/a \ \ \ \ - \${PORT_JUPYTER}:\${PORT_JUPYTER}" ./docker/docker-compose.yaml
        ;;
    TENSORBOARD)
        sed -i "/\${PORT_GOOGLE}:\${PORT_GOOGLE}/d" ./docker/docker-compose.yaml
        PORT_TOOL="\${PORT_GOOGLE}:\${PORT_GOOGLE}"
        sed -i "/^ *- ${PORT_LINE}/a \ \ \ \ - \${PORT_GOOGLE}:\${PORT_GOOGLE}" ./docker/docker-compose.yaml
        ;;
    *)
        echo "Invalid service"
        exit 1
        ;;
esac

# Remove existing lines containing ${PORT_JUPYTER}:${PORT_JUPYTER}
#sed -i "/\${PORT_JUPYTER}:\${PORT_JUPYTER}/d" ./docker/docker-compose.yaml
#sed -i "/\${PORT_GOOGLE}:\${PORT_GOOGLE}/d" ./docker/docker-compose.yaml

# Insert new port line below the appropriate port line
# Assuming the port is to be added under the 'ports' section of the service
#sed -i "/^ *- ${PORT_LINE}/a \ \ \ \ - \${PORT_JUPYTER}:\${PORT_JUPYTER}" ./docker/docker-compose.yaml

echo "Port added successfully."
