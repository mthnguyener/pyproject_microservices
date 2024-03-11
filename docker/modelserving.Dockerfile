FROM nvcr.io/nvidia/pytorch:23.11-py3

ENV TORCH_HOME=/usr/src/service_modelserving/cache

WORKDIR /usr/src/service_modelserving

COPY ../service_modelserving .

RUN pip install --upgrade pip \
#	&& pip install -e .[all] \
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

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT_MODELSERVING"]
