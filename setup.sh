#!/bin/bash

# Euromask Docker Setup Script

echo "🚀 Euromask Docker Setup"
echo "========================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data exports
chmod 755 data exports

# Build the images
echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "🎉 Setup complete! You can now run Euromask:"
echo ""
echo "📱 Web UI:"
echo "   docker-compose --profile web up"
echo "   Then visit: http://localhost:5000"
echo ""
echo "💻 CLI (Interactive):"
echo "   docker run -it --rm euromask-cli cli"
echo ""
echo "🎭 Demo:"
echo "   docker run --rm euromask-cli demo"
echo ""
echo "📊 Status:"
echo "   docker run --rm euromask-cli status"
echo ""
echo "📤 Export:"
echo "   docker run --rm euromask-cli export"
echo ""
echo "For more information, see DOCKER_README.md" 