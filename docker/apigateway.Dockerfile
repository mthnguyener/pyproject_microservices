FROM python:3.10-slim

WORKDIR /usr/src/service_apigateway

COPY ../service_apigateway .

RUN pip3 install --upgrade pip \
	&& pip3 install --no-cache-dir -r requirements.txt \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT_APIGATEWAY"]
