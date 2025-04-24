FROM python:3.11-slim
WORKDIR /srv/backend
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY src .
EXPOSE 5000
CMD ["python", "server.py"]