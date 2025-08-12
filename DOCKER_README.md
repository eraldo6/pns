# Euromask - Docker Setup

This Docker setup allows you to run Euromask without installing any dependencies on your system.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd euromask
```

### 2. Run the Web UI
```bash
docker-compose --profile web up --build
```
Then open your browser to: http://localhost:5000

### 3. Run the CLI
```bash
docker-compose --profile cli up --build
```

## Available Services

### Web UI
```bash
# Start the web interface
docker-compose --profile web up --build

# Stop the web interface
docker-compose --profile web down
```

### CLI (Interactive)
```bash
# Start interactive CLI
docker-compose --profile cli up --build

# Run CLI with specific command
docker-compose --profile cli run --rm euromask-cli cli
```

### Demo
```bash
# Run the comprehensive demo
docker-compose --profile demo up --build
```

### Status Check
```bash
# Check system status
docker-compose --profile status up --build
```

### Export Data
```bash
# Export all system data
docker-compose --profile export up --build
```

## Direct Docker Commands

If you prefer using Docker directly:

### Build the Images
```bash
# Build CLI image
docker build -t euromask-cli .

# Build Web UI image
docker build -f ui/Dockerfile -t euromask-web .
```

### Run CLI
```bash
# Interactive CLI
docker run -it --rm euromask-cli cli

# Run demo
docker run --rm euromask-cli demo

# Check status
docker run --rm euromask-cli status

# Export data
docker run --rm -v $(pwd)/exports:/app/exports euromask-cli export
```

### Run Web UI
```bash
# Start web server
docker run -p 5000:5000 --rm euromask-web
```

## Data Persistence

The Docker setup includes volume mounts for data persistence:

- `./data` - System data and JSON files
- `./exports` - Exported reports and data

## Troubleshooting

### Port 5000 Already in Use
If port 5000 is already in use, modify the `docker-compose.yml` file:
```yaml
ports:
  - "5001:5000"  # Change 5000 to 5001
```

### Permission Issues
If you encounter permission issues with volumes:
```bash
# Create data directories with proper permissions
mkdir -p data exports
chmod 755 data exports
```

### Build Issues
If the build fails, try:
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild without cache
docker-compose --profile web build --no-cache
```

## Development

For development, you can mount the source code:
```bash
docker run -it --rm \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/tests:/app/tests \
  euromask-cli cli
```

## Environment Variables

You can set environment variables in the `docker-compose.yml`:
```yaml
environment:
  - FLASK_ENV=development
  - DEBUG=true
```

## Security Notes

- The Docker containers run as root by default
- For production, consider using non-root users
- Data volumes are mounted from the host system
- Exposed ports should be restricted in production

## Support

If you encounter issues:
1. Check Docker and Docker Compose versions
2. Ensure ports are not already in use
3. Verify the repository structure is correct
4. Check the logs: `docker-compose logs [service-name]` 