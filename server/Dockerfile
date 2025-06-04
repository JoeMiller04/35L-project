FROM python:3.11-slim

# Set working directory to parent of server folder
WORKDIR /app
COPY server/requirements.txt ./server/
RUN pip install --no-cache -r server/requirements.txt

# Copy everything to maintain directory structure
COPY . .

# Expose the port
EXPOSE 8000

# Run the app with the correct module path
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]