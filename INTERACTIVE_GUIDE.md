# 🔐 Privacy Network System - Interactive Guide

A comprehensive guide with terminal commands for all scenarios and use cases of the Privacy Network System.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Operations](#basic-operations)
3. [Wallet Management](#wallet-management)
4. [Token Operations](#token-operations)
5. [Voucher System](#voucher-system)
6. [Transaction Types](#transaction-types)
7. [Offline Transfers](#offline-transfers)
8. [Compliance & AML](#compliance--aml)
9. [Privacy Ledger](#privacy-ledger)
10. [Zero-Knowledge Proofs](#zero-knowledge-proofs)
11. [Data Export](#data-export)
12. [Advanced Scenarios](#advanced-scenarios)
13. [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure Python 3.8+ is installed
python3 --version

# No external dependencies required - uses only standard library
```

### Basic Commands
```bash
# Run comprehensive demo
python3 src/main.py --demo

# Start interactive CLI
python3 src/main.py --interactive

# Check system status
python3 src/main.py --status

# Export all data
python3 src/main.py --export
```

## 🎯 Basic Operations

### Scenario 1: System Overview
```bash
# Start interactive CLI
python3 src/main.py --interactive

# Check system status
status

# View help
help

# Exit CLI
exit
```

**Expected Output:**
```
🔐 PNS> status
📊 System Status:
==============================
👛 Wallets: 0
🪙 Tokens: 0 (€0)
🎫 Vouchers: 0 (0 available)
💸 Transactions: 0 (0 anonymous)
🚨 AML Flagged: 0
📱 Offline: 0 (0 pending)
🔐 ZKP Proofs: 0
```

## 👛 Wallet Management

### Scenario 2: Create and Manage Wallets
```bash
# Create wallets
wallet create
wallet create
wallet create

# List all wallets
wallet list

# Get wallet details
wallet info <wallet_id>

# Check wallet balance
wallet balance <wallet_id>
```

**Expected Output:**
```
🔐 PNS> wallet create
✅ Created wallet: 12345678-1234-1234-1234-123456789abc
   Public Key: a1b2c3d4e5f6...

🔐 PNS> wallet list
👛 Wallets (3):
  12345678... - €0 (0 tokens, 0 vouchers)
  87654321... - €0 (0 tokens, 0 vouchers)
  abcdef12... - €0 (0 tokens, 0 vouchers)
```

## 🪙 Token Operations

### Scenario 3: Issue and Transfer Tokens
```bash
# Issue tokens to wallets
token issue <wallet_id> 50
token issue <wallet_id> 100
token issue <wallet_id> 25

# List all tokens
token list

# Check token details
token info <token_id>

# Check wallet token balance
token balance <wallet_id>
```

**Expected Output:**
```
🔐 PNS> token issue 12345678-1234-1234-1234-123456789abc 50
✅ Issued token: a1b2c3d4... - €50

🔐 PNS> token list
🪙 Tokens (3):
  a1b2c3d4... - €50 (Owner: 12345678...)
  e5f6g7h8... - €100 (Owner: 87654321...)
  i9j0k1l2... - €25 (Owner: abcdef12...)
```

## 🎫 Voucher System

### Scenario 4: Issue and Use Anonymity Vouchers
```bash
# Issue vouchers to wallets
voucher issue <wallet_id> 50
voucher issue <wallet_id> 100

# List all vouchers
voucher list

# Check voucher details
voucher info <voucher_id>

# Check available vouchers for wallet
voucher available <wallet_id>
```

**Expected Output:**
```
🔐 PNS> voucher issue 12345678-1234-1234-1234-123456789abc 50
✅ Issued voucher: m3n4o5p6... - €50 limit

🔐 PNS> voucher list
🎫 Vouchers (2):
  m3n4o5p6... - €50 limit (Available)
  q7r8s9t0... - €100 limit (Available)
```

## 💸 Transaction Types

### Scenario 5: Regular (Non-Anonymous) Transfer
```bash
# Execute regular transfer
transfer <sender_wallet_id> <receiver_wallet_id> <token_id>

# List all transactions
transfer list

# Get transaction details
transfer info <transaction_id>
```

**Expected Output:**
```
🔐 PNS> transfer 12345678-1234-1234-1234-123456789abc 87654321-1234-1234-1234-123456789abc a1b2c3d4-e5f6-7890-abcd-123456789abc
✅ Transfer completed: u1v2w3x4...

🔐 PNS> transfer list
💸 Transactions (1):
  ✅ u1v2w3x4... - 12345678... → 87654321... 👁️
```

### Scenario 6: Anonymous Transfer
```bash
# Execute anonymous transfer with voucher
transfer anonymous <sender_wallet_id> <receiver_wallet_id> <token_id> <voucher_id>
```

**Expected Output:**
```
🔐 PNS> transfer anonymous 87654321-1234-1234-1234-123456789abc abcdef12-1234-1234-1234-123456789abc e5f6g7h8-i9j0-klmn-opqr-123456789abc m3n4o5p6-q7r8-stuv-wxyz-123456789abc
✅ Anonymous transfer completed: y5z6a7b8...
```

## 📱 Offline Transfers

### Scenario 7: Peer-to-Peer Offline Transfer
```bash
# Create offline transaction
offline create <sender_wallet_id> <receiver_wallet_id> <token_id>

# List offline transactions
offline list

# Sign offline transaction (simulated)
offline sign <offline_id> <wallet_id> <signature>

# Sync with ledger
offline sync <offline_id>
```

**Expected Output:**
```
🔐 PNS> offline create 12345678-1234-1234-1234-123456789abc 87654321-1234-1234-1234-123456789abc a1b2c3d4-e5f6-7890-abcd-123456789abc
✅ Offline transaction created: c9d0e1f2...
   Status: pending

🔐 PNS> offline list
📱 Offline Transactions (1):
  📝 c9d0e1f2... - 12345678... → 87654321... (€50)
```

## 🚨 Compliance & AML

### Scenario 8: Monitor Compliance
```bash
# List AML entries
compliance list

# Check compliance statistics
compliance stats

# Export AML report
compliance export
```

**Expected Output:**
```
🔐 PNS> compliance list
🚨 AML Entries (2):
  u1v2w3x4... - €50 (Risk: 0.30)
  y5z6a7b8... - €100 (Risk: 0.70) 🚨

🔐 PNS> compliance stats
📊 Compliance Statistics:
  Total Flagged: 2
  High Risk: 1
  Escalated: 1
  Authority Contacted: Yes
  Average Risk Score: 0.50
```

## 📋 Privacy Ledger

### Scenario 9: Audit Trail
```bash
# List ledger entries
ledger list

# Check ledger statistics
ledger stats

# Export ledger data
ledger export
```

**Expected Output:**
```
🔐 PNS> ledger list
📋 Ledger Entries (3):
  🔒 0 - €50 (anonymous)
  👁️ 1 - €100 (non_anonymous)
  🔒 2 - €25 (anonymous)

🔐 PNS> ledger stats
📊 Ledger Statistics:
  Total Entries: 3
  Anonymous: 2 (66.7%)
  Non-Anonymous: 1
  AML Flagged: 0
  Total Value: €175
  Anonymous Value: €75 (42.9%)
```

## 🔐 Zero-Knowledge Proofs

### Scenario 10: Privacy Verification
```bash
# Generate range proof
zkp range <wallet_id> <min_value> <max_value>

# Verify proof
zkp verify <proof_id>

# List all proofs
zkp list

# Check ZKP statistics
zkp stats
```

**Expected Output:**
```
🔐 PNS> zkp range 12345678-1234-1234-1234-123456789abc 0 200
✅ Range proof generated: g3h4i5j6...
   Range: €0 - €200

🔐 PNS> zkp list
🔐 ZKP Proofs (1):
  ✅ g3h4i5j6... - range_proof

🔐 PNS> zkp stats
📊 ZKP Statistics:
  Total Proofs: 1
  Verified: 1
  Unverified: 0
  Verification Rate: 100.0%
  Proof Types:
    range_proof: 1
```

## 📤 Data Export

### Scenario 11: Export System Data
```bash
# Export all data
export all

# Export specific data types
export aml
export ledger
export zkp
```

**Expected Output:**
```
🔐 PNS> export all
✅ System data exported:
   AML Report: aml_report_20250101_120000.json
   Ledger Export: aml_loggable_transactions_20250101_120000.json
   Volume Report: volume_report_20250101_120000.json
   Offline Transactions: offline_transactions_20250101_120000.json
   ZKP Proofs: zkp_proofs_20250101_120000.json
```

## 🔬 Advanced Scenarios

### Scenario 12: Research Use Case
```bash
# Run comprehensive demo
python3 src/main.py --demo

# Check system status
python3 src/main.py --status

# Export all data for analysis
python3 src/main.py --export
```

**Expected Output:**
```
🎭 Privacy Network System - Comprehensive Demo
==================================================
1️⃣ Creating wallets...
   ✅ Created 3 wallets
2️⃣ Issuing tokens...
   ✅ Issued tokens: €50, €100, €25
3️⃣ Issuing anonymity vouchers...
   ✅ Issued vouchers with limits: €50, €100
4️⃣ Executing regular transfer...
   ✅ Regular transfer completed (AML flagged)
5️⃣ Executing anonymous transfer...
   ✅ Anonymous transfer completed
6️⃣ Creating offline transfer...
   ✅ Offline transfer created
7️⃣ Generating zero-knowledge proof...
   ✅ Range proof generated
8️⃣ System Status:
   Wallets: 3
   Tokens: 3 (€175)
   Vouchers: 2 (1 available)
   Transactions: 2 (1 anonymous)
   AML Flagged: 1
   Offline: 1 (1 pending)
   ZKP Proofs: 1
✅ Demo completed successfully!
```

### Scenario 13: Compliance Testing
```bash
# Create high-value transaction (should be flagged)
transfer <wallet1> <wallet2> <high_value_token>

# Create anonymous transaction (should be flagged)
transfer anonymous <wallet1> <wallet2> <token> <voucher>

# Check compliance results
compliance list
compliance stats
```

### Scenario 14: Privacy Analysis
```bash
# Generate multiple ZKP proofs
zkp range <wallet_id> 0 100
zkp range <wallet_id> 50 150
zkp range <wallet_id> 0 200

# Verify all proofs
zkp verify <proof_id1>
zkp verify <proof_id2>
zkp verify <proof_id3>

# Analyze privacy statistics
ledger stats
zkp stats
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Wallet not found"
```bash
# Solution: Create wallet first
wallet create
# Then use the returned wallet ID
```

#### Issue 2: "Token not found"
```bash
# Solution: Issue token first
token issue <wallet_id> <value>
# Then use the returned token ID
```

#### Issue 3: "Voucher not found"
```bash
# Solution: Issue voucher first
voucher issue <wallet_id> <limit>
# Then use the returned voucher ID
```

#### Issue 4: "Sender does not own token"
```bash
# Solution: Ensure token is owned by sender
token balance <sender_wallet_id>
# Transfer token to sender if needed
```

#### Issue 5: "Voucher cannot be used for value"
```bash
# Solution: Check voucher limit
voucher info <voucher_id>
# Use voucher with appropriate value limit
```

### Debug Commands
```bash
# Check system status
status

# List all components
wallet list
token list
voucher list
transfer list
offline list
compliance list
ledger list
zkp list

# Export data for analysis
export all
```

### Performance Tips
```bash
# Use shorter wallet/token IDs in commands
# Copy-paste IDs from list commands
# Use tab completion if available
# Check help for command syntax
help
```

## 📊 Expected File Structure

After running the system, you should see these files:
```
pns/
├── src/
│   ├── *.py                    # Source code
├── tests/
│   └── demo_scenarios.py       # Test scenarios
├── privacy_ledger.json         # Ledger data
├── aml_report_*.json          # AML reports
├── volume_report_*.json       # Volume reports
├── offline_transactions_*.json # Offline data
├── zkp_proofs_*.json         # ZKP proofs
└── requirements.txt           # Dependencies
```

## 🎯 Key Features Demonstrated

1. **Pseudonymous Wallets**: UUID-based identification
2. **Digital Tokens**: Euro-denominated currency
3. **Anonymity Vouchers**: Privacy layer with AML approval
4. **AML Compliance**: Risk scoring and flagging
5. **Offline Transfers**: Peer-to-peer transactions
6. **Privacy Ledger**: Audit trail with privacy
7. **Zero-Knowledge Proofs**: Cryptographic verification
8. **Data Export**: Regulatory reporting capabilities

## 🔐 Privacy Features

- **Pseudonymity**: No real-world identity linkage
- **Anonymity**: Voucher-based privacy with limits
- **Audit Trail**: Privacy-preserving ledger
- **Compliance**: AML monitoring without compromising privacy
- **Offline Capability**: Cash-like peer-to-peer transfers

## 🚨 Compliance Features

- **Risk Scoring**: Multi-factor risk assessment
- **Transaction Flagging**: Automatic suspicious activity detection
- **Authority Escalation**: High-risk transaction notification
- **Regulatory Reporting**: Export capabilities for authorities
- **Audit Trail**: Complete transaction history

---

**🔐 Privacy Network System** - Balancing privacy with compliance in digital currency systems. 