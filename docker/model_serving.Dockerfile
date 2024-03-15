FROM nvcr.io/nvidia/pytorch:23.11-py3

ENV TORCH_HOME=/usr/src/model_serving/cache

WORKDIR /usr/src/model_serving

COPY ../pyproject_microservices/model_serving .

RUN pip install --upgrade pip \
	&& pip install -e .[all] \
	&& apt update -y \
	# && apt -y upgrade \
	&& apt install -y \
		fonts-humor-sans \
    && pip install --no-cache-dir -r \
        requirements.txt \
	# && conda update -y conda \
	# && while read requirement; do conda install --yes ${requirement}; done < requirements_pytorch.txt \
	# Clean up
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

ENV PYTHONPATH=/usr/src/model_serving/model_serving
ENV PYTHONPATH=/usr/src/model_serving/model_serving/utils

CMD ["sh", "-c", "uvicorn model_serving.app:model_serving_app --host 0.0.0.0 --port $PORT_MODELSERVING"]
