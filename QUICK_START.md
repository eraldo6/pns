# Euromask - Quick Start Guide

## 🚀 **One-Command Setup**

```bash
# Run the automated setup
./setup.sh
```

## 📱 **Web UI (Browser Interface)**

```bash
# Start the web interface
docker-compose --profile web up

# Open your browser to: http://localhost:5000
```

## 💻 **CLI (Command Line Interface)**

```bash
# Build the CLI image (one-time setup)
docker build -t euromask-cli .

# Run CLI interactively
docker run -it --rm euromask-cli cli
```

## 🎭 **Demo (One-time run)**

```bash
# Run the comprehensive demo
docker run --rm euromask-cli demo
```

## 🔧 **Other Commands**

```bash
# Check system status
docker run --rm euromask-cli status

# Export all data
docker run --rm euromask-cli export
```

## 🎯 **Quick Examples**

### **Web UI**
1. Run: `docker-compose --profile web up`
2. Open: http://localhost:5000
3. Use the web interface to create wallets, tokens, and execute transactions

### **CLI Interactive**
```bash
docker run -it --rm euromask-cli cli

# In the CLI:
> wallet create
> token issue <wallet_id> 100
> transfer <sender> <receiver> <token_id>
> exit
```

### **Demo**
```bash
docker run --rm euromask-cli demo
```

## 🆘 **Troubleshooting**

### **Port 5000 Already in Use**
Edit `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Change 5000 to 5001
```

### **Docker Not Running**
- Start Docker Desktop
- Wait for it to fully initialize

### **Permission Issues**
```bash
mkdir -p data exports
chmod 755 data exports
```

## 📋 **What's Included**

- ✅ **Privacy-Preserving Wallets**: Pseudonymous digital wallets
- ✅ **Token System**: Euro-denominated digital currency
- ✅ **Anonymity Vouchers**: Privacy layer for transactions
- ✅ **AML Compliance**: Automatic monitoring and flagging
- ✅ **Offline Transfers**: Peer-to-peer without immediate ledger access
- ✅ **Zero-Knowledge Proofs**: Cryptographic privacy verification
- ✅ **Modern Web UI**: Real-time interface with Socket.IO
- ✅ **Comprehensive CLI**: Full command-line interface
- ✅ **High-Value AML Demo**: €10,000+ transactions trigger monitoring

## 🎉 **Ready to Use!**

Both the web UI and CLI are now working correctly. Choose your preferred interface and start exploring Euromask! 