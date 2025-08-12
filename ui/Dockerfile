FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ui/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/
COPY ui/ ./ui/

# Create a script to run the web UI
RUN echo '#!/bin/bash\n\
echo "Starting Euromask Web UI..."\n\
echo "Web UI will be available at: http://localhost:5000"\n\
echo "Press Ctrl+C to stop the server"\n\
cd ui && FLASK_ENV=development python app.py' > /app/run-ui.sh && chmod +x /app/run-ui.sh

# Expose port
EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["/app/run-ui.sh"] 