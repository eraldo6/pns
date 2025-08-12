FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/
COPY tests/ ./tests/

# Create a script to run the application
RUN echo '#!/bin/bash\n\
if [ "$1" = "cli" ]; then\n\
    echo "Starting Euromask CLI..."\n\
    python3 src/main.py --interactive\n\
elif [ "$1" = "demo" ]; then\n\
    echo "Running Euromask Demo..."\n\
    python3 src/main.py --demo\n\
elif [ "$1" = "status" ]; then\n\
    echo "Showing Euromask Status..."\n\
    python3 src/main.py --status\n\
elif [ "$1" = "export" ]; then\n\
    echo "Exporting Euromask Data..."\n\
    python3 src/main.py --export\n\
else\n\
    echo "Usage: docker run euromask [cli|demo|status|export]"\n\
    echo "  cli    - Start interactive CLI"\n\
    echo "  demo   - Run comprehensive demo"\n\
    echo "  status - Show system status"\n\
    echo "  export - Export all data"\n\
fi' > /app/run.sh && chmod +x /app/run.sh

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]
CMD ["cli"] 