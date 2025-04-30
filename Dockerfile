FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Build the MkDocs site
RUN mkdocs build

# Expose port for the Flask app
EXPOSE 5000

# Run the server
CMD ["python", "server.py"]