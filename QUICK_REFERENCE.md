# 🔐 Privacy Network System - Quick Reference

## 🚀 Quick Start Commands

```bash
# Run demo
python3 src/main.py --demo

# Interactive CLI
python3 src/main.py --interactive

# System status
python3 src/main.py --status

# Export data
python3 src/main.py --export

# Run tests
python3 tests/demo_scenarios.py
```

## 📊 System Status Output

```
📊 System Status:
==============================
👛 Wallets: 3
🪙 Tokens: 3 (€175)
🎫 Vouchers: 2 (1 available)
💸 Transactions: 2 (1 anonymous)
🚨 AML Flagged: 1
📱 Offline: 1 (1 pending)
🔐 ZKP Proofs: 1
```

## 🎯 Essential CLI Commands

### System Commands
```bash
status                    # Show system status
help                      # Show help
exit/quit                 # Exit CLI
demo                      # Run comprehensive demo
```

### Wallet Commands
```bash
wallet create             # Create new wallet
wallet list               # List all wallets
wallet info <id>          # Show wallet details
wallet balance <id>       # Show wallet balance
```

### Token Commands
```bash
token issue <wallet_id> <value>  # Issue token
token list                        # List all tokens
token info <id>                   # Show token details
token balance <wallet_id>         # Show wallet's tokens
```

### Voucher Commands
```bash
voucher issue <wallet_id> <limit> # Issue voucher
voucher list                       # List all vouchers
voucher info <id>                  # Show voucher details
voucher available <wallet_id>      # Show available vouchers
```

### Transfer Commands
```bash
transfer <sender> <receiver> <token_id> [voucher_id]  # Execute transfer
transfer list                       # List all transactions
transfer info <id>                  # Show transaction details
transfer anonymous <sender> <receiver> <token_id> <voucher_id>  # Anonymous transfer
```

### Offline Commands
```bash
offline create <sender> <receiver> <token_id> [voucher_id]  # Create offline transaction
offline sign <offline_id> <wallet_id> <signature>           # Sign offline transaction
offline sync <offline_id>                                   # Sync with ledger
offline list                                                 # List offline transactions
```

### Compliance Commands
```bash
compliance list             # List AML entries
compliance stats            # Show compliance statistics
compliance export           # Export AML report
```

### Ledger Commands
```bash
ledger list                 # List ledger entries
ledger stats                # Show ledger statistics
ledger export               # Export ledger data
```

### ZKP Commands
```bash
zkp range <wallet_id> <min> <max>     # Generate range proof
zkp verify <proof_id>                 # Verify proof
zkp list                               # List all proofs
zkp stats                              # Show ZKP statistics
```

### Export Commands
```bash
export all                # Export all system data
export aml                # Export AML report
export ledger             # Export ledger data
export zkp                # Export ZKP proofs
```

## 🔧 Common Workflows

### 1. Basic Setup
```bash
python3 src/main.py --interactive
wallet create
wallet create
token issue <wallet1> 50
token issue <wallet2> 100
voucher issue <wallet1> 50
```

### 2. Regular Transfer
```bash
transfer <wallet1> <wallet2> <token_id>
transfer list
```

### 3. Anonymous Transfer
```bash
transfer anonymous <wallet1> <wallet2> <token_id> <voucher_id>
compliance list
```

### 4. Offline Transfer
```bash
offline create <wallet1> <wallet2> <token_id>
offline list
offline sync <offline_id>
```

### 5. Privacy Verification
```bash
zkp range <wallet_id> 0 200
zkp verify <proof_id>
zkp stats
```

### 6. Compliance Monitoring
```bash
compliance list
compliance stats
compliance export
```

### 7. Data Export
```bash
export all
ledger stats
```

## 📋 Expected Outputs

### Wallet Creation
```
✅ Created wallet: 12345678-1234-1234-1234-123456789abc
   Public Key: a1b2c3d4e5f6...
```

### Token Issuance
```
✅ Issued token: a1b2c3d4... - €50
```

### Voucher Issuance
```
✅ Issued voucher: m3n4o5p6... - €50 limit
```

### Transfer Execution
```
✅ Transfer completed: u1v2w3x4...
🚨 Transaction flagged for AML monitoring
```

### Anonymous Transfer
```
✅ Anonymous transfer completed: y5z6a7b8...
```

### Offline Transaction
```
✅ Offline transaction created: c9d0e1f2...
   Status: pending
```

### ZKP Proof
```
✅ Range proof generated: g3h4i5j6...
   Range: €0 - €200
```

### Compliance Alert
```
🚨 HIGH RISK TRANSACTION ESCALATED TO AUTHORITY:
   Transaction ID: test_tx_123
   Amount: €150
   Risk Score: 1.0
   Reason: High value transaction: €150; Non-anonymous transaction
```

## 🔐 Key Features

### Privacy Features
- **Pseudonymity**: UUID-based wallet identification
- **Anonymity**: Voucher-based privacy with limits
- **Audit Trail**: Privacy-preserving ledger
- **Offline Capability**: Peer-to-peer transfers

### Compliance Features
- **Risk Scoring**: Multi-factor assessment
- **Transaction Flagging**: Automatic detection
- **Authority Escalation**: High-risk notifications
- **Regulatory Reporting**: Export capabilities

### Technical Features
- **Zero-Knowledge Proofs**: Cryptographic verification
- **Dual Signatures**: Offline transaction security
- **AML Monitoring**: Real-time compliance checking
- **Data Export**: JSON-based reporting

## 🚨 Risk Scoring

| Factor | Risk Score | Threshold |
|--------|------------|-----------|
| High Value (>€100) | +0.7 | Flagged |
| Non-Anonymous | +0.3 | Flagged |
| Suspicious Pattern | +0.5 | Flagged |
| **Total** | **≥0.5** | **Flagged** |
| **Total** | **≥0.8** | **Escalated** |

## 📊 File Structure

```
pns/
├── src/
│   ├── wallet.py          # Wallet system
│   ├── token_system.py    # Token management
│   ├── voucher.py         # Anonymity vouchers
│   ├── transaction.py     # Transfer engine
│   ├── compliance.py      # AML compliance
│   ├── ledger.py          # Privacy ledger
│   ├── offline.py         # Offline transfers
│   ├── zkp.py            # Zero-knowledge proofs
│   ├── cli.py            # Command interface
│   └── main.py           # System coordinator
├── tests/
│   └── demo_scenarios.py  # Test scenarios
├── privacy_ledger.json    # Ledger data
├── aml_report_*.json     # AML reports
├── volume_report_*.json  # Volume reports
├── offline_transactions_*.json # Offline data
├── zkp_proofs_*.json    # ZKP proofs
└── requirements.txt      # Dependencies
```

## 🔧 Troubleshooting

### Common Errors
- **"Wallet not found"** → Create wallet first
- **"Token not found"** → Issue token first
- **"Voucher not found"** → Issue voucher first
- **"Sender does not own token"** → Check token ownership
- **"Voucher cannot be used for value"** → Check voucher limit

### Debug Commands
```bash
status                    # Check system status
wallet list              # List all wallets
token list               # List all tokens
voucher list             # List all vouchers
transfer list            # List all transactions
compliance list          # List AML entries
ledger list              # List ledger entries
zkp list                 # List ZKP proofs
export all               # Export all data
```

### Performance Tips
- Use shorter IDs in commands
- Copy-paste IDs from list commands
- Check help for command syntax
- Use tab completion if available

## 🎯 Research Scenarios

### 1. Privacy Analysis
```bash
python3 src/main.py --demo
ledger stats
zkp stats
export all
```

### 2. Compliance Testing
```bash
# Create high-value transactions
transfer <wallet1> <wallet2> <high_value_token>
compliance list
compliance stats
```

### 3. Offline Capability
```bash
offline create <sender> <receiver> <token>
offline list
offline sync <offline_id>
```

### 4. ZKP Verification
```bash
zkp range <wallet_id> 0 200
zkp verify <proof_id>
zkp stats
```

---

**🔐 Privacy Network System** - Quick reference for digital currency with privacy features. 