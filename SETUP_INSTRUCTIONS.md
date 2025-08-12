# Euromask - Setup Instructions

## 🚀 Quick Setup (Docker - Recommended)

### Prerequisites
- Docker Desktop installed and running
- Docker Compose (usually comes with Docker Desktop)

### Steps
1. **Clone/Download** the Euromask project
2. **Open terminal** in the project directory
3. **Run setup script**:
   ```bash
   ./setup.sh
   ```
4. **Start the application**:

   **For Web UI:**
   ```bash
   docker-compose --profile web up
   ```
   Then open: http://localhost:5000

   **For CLI:**
   ```bash
   docker run -it --rm euromask-cli cli
   ```

   **For Demo:**
   ```bash
   docker run --rm euromask-cli demo
   ```

## 📱 What You Can Do

### Web Interface
- Create wallets, tokens, and vouchers
- Execute transactions
- View system status
- Run comprehensive demo
- Export data

### Command Line Interface
- Interactive commands for all features
- Create wallets: `wallet create`
- Issue tokens: `token issue <wallet_id> <value>`
- Execute transfers: `transfer <sender> <receiver> <token_id>`
- Run demo: `demo`

## 🎭 Demo Features

The demo includes:
- ✅ Wallet creation
- ✅ Token issuance
- ✅ Voucher creation
- ✅ Regular transfers
- ✅ Anonymous transfers
- ✅ **AML-flagged high-value transactions** (€10,000+)
- ✅ Offline transfers
- ✅ Zero-knowledge proofs

## 🔧 Troubleshooting

### Port 5000 Already in Use
If you get a port conflict, edit `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Change 5000 to 5001
```

### Docker Not Running
Make sure Docker Desktop is started before running commands.

### Permission Issues
```bash
mkdir -p data exports
chmod 755 data exports
```

## 📁 Project Structure

```
euromask/
├── src/                    # Core system code
├── ui/                     # Web interface
├── tests/                  # Test scenarios
├── data/                   # Persistent data (created by Docker)
├── exports/                # Exported reports (created by Docker)
├── docker-compose.yml      # Docker services
├── Dockerfile              # Main application container
├── ui/Dockerfile           # Web UI container
├── setup.sh               # Setup script
└── DOCKER_README.md       # Detailed Docker documentation
```

## 🆘 Need Help?

1. Check `DOCKER_README.md` for detailed instructions
2. Ensure Docker Desktop is running
3. Try the setup script: `./setup.sh`
4. Check logs: `docker-compose logs [service-name]`

## 🎯 Key Features

- **Privacy-Preserving**: Pseudonymous wallets and anonymous transactions
- **AML Compliance**: Automatic monitoring and flagging of suspicious transactions
- **Offline Capable**: Peer-to-peer transfers without immediate ledger access
- **Zero-Knowledge Proofs**: Cryptographic privacy verification
- **Modern UI**: Web interface with real-time updates
- **Comprehensive CLI**: Full command-line interface

Enjoy exploring Euromask! 🎉 