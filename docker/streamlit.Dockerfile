FROM python:3.10

WORKDIR /usr/src/pyproject_microservices/pyproject_microservices/streamlit

COPY ../pyproject_microservices/streamlit .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/pyproject_microservices/pyproject_microservices

COPY ../pyproject_microservices/streamlit/__init__.py .

ENV PYTHONPATH=/usr/src/pyproject_microservices

CMD ["streamlit", "run", "streamlit/app.py"]
