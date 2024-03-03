FROM python:3.10

WORKDIR /usr/src/service_frontend

COPY ../service_frontend .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/service_frontend

ENV PYTHONPATH=/usr/src/service_frontend

CMD ["streamlit", "run", "app.py"]
