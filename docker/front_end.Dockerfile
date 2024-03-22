FROM python:3.10-slim

WORKDIR /usr/src/front_end

COPY ../pyproject_microservices/front_end .

RUN pip install --upgrade pip \
	&& pip install -e .[all] \
    && pip install --no-cache-dir -r \
        requirements.txt \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

ENV PYTHONPATH=/usr/src/front_end/front_end
ENV PYTHONPATH=/usr/src/front_end/front_end/utils

CMD streamlit run --server.port $PORT_FRONTEND front_end/app.py

