FROM python:3.10-slim

WORKDIR /usr/src/api_gateway

COPY ../pyproject_microservices/api_gateway .

RUN pip install --upgrade pip \
    && pip install -e .[all] \
    && apt update -y \
#    && apt -y upgrade \
#    && apt-get install -y \
    && pip install --no-cache-dir -r \
        requirements.txt \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y \

ENV PYTHONPATH=/usr/src/api_gateway/api_gateway
ENV PYTHONPATH=/usr/src/api_gateway/api_gateway/utils

CMD ["sh", "-c", "uvicorn api_gateway.app:api_gateway_app --host 0.0.0.0 --port $PORT_APIGATEWAY"]
