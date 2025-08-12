# Euromask CLI Commands

## 🖥️ **Running CLI Interactively**

### **Method 1: Direct Docker Run (Recommended)**
```bash
# Run CLI interactively
docker run -it --rm euromask-cli cli

# Or with data persistence
docker run -it --rm -v $(pwd)/data:/app/data euromask-cli cli
```

### **Method 2: Docker Compose with Interactive Mode**
```bash
# Run CLI interactively
docker-compose --profile cli run --rm euromask-cli cli

# Or run the service and attach to it
docker-compose --profile cli up -d
docker attach euromask-cli
```

### **Method 3: Execute Commands Directly**
```bash
# Run specific commands without entering CLI
docker run --rm euromask-cli demo
docker run --rm euromask-cli status
docker run --rm euromask-cli export
```

## 💻 **Available CLI Commands**

Once you're in the interactive CLI, you can use:

### **Wallet Commands**
```
wallet create                    # Create a new wallet
wallet list                      # List all wallets
wallet show <wallet_id>          # Show wallet details
```

### **Token Commands**
```
token issue <wallet_id> <value>  # Issue a new token
token list                       # List all tokens
token show <token_id>            # Show token details
```

### **Voucher Commands**
```
voucher issue <wallet_id> <limit> # Issue a new voucher
voucher list                     # List all vouchers
voucher show <voucher_id>        # Show voucher details
```

### **Transaction Commands**
```
transfer <sender> <receiver> <token_id> [--anonymous]  # Execute transfer
transaction list                 # List all transactions
transaction show <tx_id>         # Show transaction details
```

### **System Commands**
```
demo                             # Run comprehensive demo
status                           # Show system status
export                           # Export all data
help                             # Show available commands
exit                             # Exit CLI
```

## 🎯 **Quick Examples**

### **Create and Use Wallets**
```bash
# Start CLI
docker run -it --rm euromask-cli cli

# In CLI:
wallet create
wallet create
wallet list
```

### **Issue and Transfer Tokens**
```bash
# In CLI:
token issue <wallet_id> 100
transfer <sender_wallet_id> <receiver_wallet_id> <token_id>
```

### **Run Demo**
```bash
# Direct command
docker run --rm euromask-cli demo

# Or in CLI:
demo
```

## 🔧 **Troubleshooting**

### **CLI Not Responding**
- Make sure you're using `-it` flags
- Try `docker run -it --rm euromask-cli cli`

### **Data Not Persisting**
- Use volume mount: `-v $(pwd)/data:/app/data`

### **Commands Not Working**
- Check wallet/token IDs exist first
- Use `list` commands to see available items

## 📝 **Example Session**

```bash
$ docker run -it --rm euromask-cli cli

Starting Euromask CLI...
Euromask - Interactive CLI
==================================================
Type 'help' for available commands
Type 'exit' to quit

> wallet create
Wallet created successfully!
Wallet ID: abc123...
Public Key: def456...

> wallet create
Wallet created successfully!
Wallet ID: ghi789...
Public Key: jkl012...

> wallet list
Wallets:
- abc123... (0 tokens, 0 vouchers)
- ghi789... (0 tokens, 0 vouchers)

> token issue abc123... 500
Token issued successfully!
Token ID: mno345...

> transfer abc123... ghi789... mno345...
Transfer executed successfully!
Transaction ID: pqr678...

> exit
Goodbye!
``` 