@echo off
REM Euromask Docker Setup Script for Windows

echo 🚀 Euromask Docker Setup
echo ========================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Visit: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo    Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create necessary directories
echo 📁 Creating data directories...
if not exist "data" mkdir data
if not exist "exports" mkdir exports

REM Build the images
echo 🔨 Building Docker images...
docker-compose build

echo.
echo 🎉 Setup complete! You can now run Euromask:
echo.
echo 📱 Web UI:
echo    docker-compose --profile web up
echo    Then visit: http://localhost:5000
echo.
echo 💻 CLI (Interactive):
echo    docker build -t euromask-cli .
echo    docker run -it --rm euromask-cli cli
echo.
echo 🎭 Demo:
echo    docker run --rm euromask-cli demo
echo.
echo 📊 Status:
echo    docker run --rm euromask-cli status
echo.
echo 📤 Export:
echo    docker run --rm euromask-cli export
echo.
echo For more information, see DOCKER_README.md
pause 