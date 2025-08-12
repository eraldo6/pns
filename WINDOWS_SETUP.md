# Euromask - Windows Setup Guide

## 🖥️ **Windows-Specific Instructions**

### Prerequisites
- **Docker Desktop for Windows** installed and running
- **WSL2** enabled (Docker Desktop handles this automatically)
- **Windows 10/11** (64-bit)

### Step 1: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install and restart your computer
3. Start Docker Desktop from Start Menu
4. Wait for Docker to fully initialize (green icon in system tray)

### Step 2: Setup Euromask

#### Option A: Using Windows Setup Script
```cmd
# Open Command Prompt as Administrator
cd C:\path\to\euromask
setup.bat
```

#### Option B: Manual Setup
```cmd
# Open Command Prompt as Administrator
cd C:\path\to\euromask

# Create directories
mkdir data
mkdir exports

# Build images
docker-compose build
docker build -t euromask-cli .
```

### Step 3: Run the Application

#### Web UI (Recommended for Windows)
```cmd
docker-compose --profile web up
```
Then open: **http://localhost:5000**

#### CLI (Alternative)
```cmd
docker run -it --rm euromask-cli cli
```

#### Demo
```cmd
docker run --rm euromask-cli demo
```

## 🔧 **Windows Troubleshooting**

### **Docker Desktop Not Running**
- Check system tray for Docker icon
- Start Docker Desktop from Start Menu
- Wait for "Docker Desktop is running" message

### **Permission Denied Errors**
- Run Command Prompt as Administrator
- Ensure Docker Desktop has necessary permissions

### **Port 5000 Already in Use**
Edit `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Change 5000 to 5001
```

### **Path Issues**
- Use forward slashes or escaped backslashes in paths
- Ensure you're in the correct directory

### **No Output from Docker Commands**
1. Check Docker Desktop is running
2. Try: `docker --version`
3. Try: `docker ps`
4. Restart Docker Desktop if needed

### **WSL2 Issues**
- Docker Desktop should handle WSL2 automatically
- If issues persist, enable WSL2 in Windows Features

## 🎯 **Quick Windows Commands**

### **Check Docker Status**
```cmd
docker --version
docker ps
```

### **Build and Run**
```cmd
# Build images
docker-compose build

# Run web UI
docker-compose --profile web up

# Run CLI
docker run -it --rm euromask-cli cli
```

### **Stop Services**
```cmd
docker-compose down
```

## 📋 **Windows-Specific Notes**

- **File Paths**: Use Windows-style paths in Command Prompt
- **Line Endings**: Git should handle this automatically
- **Antivirus**: May need to whitelist Docker processes
- **Firewall**: Allow Docker through Windows Firewall
- **Performance**: WSL2 provides better performance than WSL1

## 🆘 **Still Having Issues?**

1. **Restart Docker Desktop**
2. **Run Command Prompt as Administrator**
3. **Check Windows Event Viewer for errors**
4. **Update Docker Desktop to latest version**
5. **Ensure Windows is up to date**

## 🎉 **Success Indicators**

- Docker Desktop shows green icon
- `docker ps` shows running containers
- Web UI loads at http://localhost:5000
- CLI responds to commands 