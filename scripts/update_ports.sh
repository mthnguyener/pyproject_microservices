#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <service>"
    exit 1
fi

# Get service name from command-line argument
SERVICE=$1

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

# Remove existing lines containing ${PORT_JUPYTER}:${PORT_JUPYTER}
sed -i "/\${PORT_JUPYTER}:\${PORT_JUPYTER}/d" ./docker/docker-compose.yaml

# Insert new port line below the appropriate port line
# Assuming the port is to be added under the 'ports' section of the service
sed -i "/^ *- ${PORT_LINE}/a \ \ \ \ - \${PORT_JUPYTER}:\${PORT_JUPYTER}" ./docker/docker-compose.yaml

echo "Port added successfully."
