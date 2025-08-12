# Euromask (PNS)

A comprehensive digital currency system with privacy features, implementing pseudonymous wallets, anonymous transactions, AML compliance, offline transfers, and zero-knowledge proofs.

## Overview

The Euromask (PNS) is a complete digital currency implementation that balances privacy with regulatory compliance. It features:

- **Pseudonymous Wallets**: Cryptographic keypairs with UUID-based identification
- **Digital Tokens**: Euro-denominated digital currency units
- **Anonymity Vouchers**: Privacy layer for anonymous transactions
- **AML Compliance**: Anti-money laundering monitoring and reporting
- **Offline Transfers**: Peer-to-peer transactions without immediate ledger access
- **Privacy Ledger**: Audit trail with privacy-preserving features
- **Zero-Knowledge Proofs**: Cryptographic privacy verification

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wallet        │    │   Token         │    │   Voucher       │
│   System        │    │   System        │    │   System        │
│                 │    │                 │    │                 │
│ • Keypair Gen   │    │ • Token Issuance│    │ • AML Authority │
│ • Balance Mgmt  │    │ • Ownership     │    │ • Value Limits  │
│ • Signing       │    │ • Transfer      │    │ • Redemption    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Transaction   │
                    │   Engine        │
                    │                 │
                    │ • Transfer Logic│
                    │ • AML Routing   │
                    │ • Ledger Logging│
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Compliance    │    │   Privacy       │    │   Offline       │
│   System        │    │   Ledger        │    │   System        │
│                 │    │                 │    │                 │
│ • AML Rules     │    │ • Audit Trail   │    │ • P2P Transfers │
│ • Risk Scoring  │    │ • Pseudonymous  │    │ • Dual Signing  │
│ • Escalation    │    │ • Export        │    │ • Sync          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ZKP System    │
                    │                 │
                    │ • Range Proofs  │
                    │ • Equality      │
                    │ • Membership    │
                    └─────────────────┘
```

## Quick Start

### Option 1: Docker (Recommended)
The easiest way to run Euromask without installing dependencies:

```bash
# Clone the repository
git clone <repository-url>
cd euromask

# Run the setup script
./setup.sh

# Start the web UI
docker-compose --profile web up

# Or run the CLI interactively
docker run -it --rm euromask-cli cli

# Or run the demo
docker run --rm euromask-cli demo
```

**Note:** For CLI commands, you need to build the image first:
```bash
docker build -t euromask-cli .
```
```

For detailed Docker instructions, see [DOCKER_README.md](DOCKER_README.md).

**Windows Users**: See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for Windows-specific instructions.

### Option 2: Local Installation
If you prefer to install dependencies locally:

#### Prerequisites
- Python 3.8+ (uses dataclasses)
- No external dependencies required

#### Installation
```bash
# Clone the repository
git clone <repository-url>
cd euromask

# Run the system
python3 src/main.py --demo
```

### Basic Usage

#### 1. Run Demo
```bash
python3 src/main.py --demo
```

#### 2. Interactive CLI
```bash
python3 src/main.py --interactive
```

#### 3. Check Status
```bash
python3 src/main.py --status
```

#### 4. Export Data
```bash
python3 src/main.py --export
```

## Project Structure

```
pns/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── wallet.py            # Wallet system
│   ├── token_system.py      # Token management
│   ├── voucher.py           # Anonymity vouchers
│   ├── transaction.py       # Transaction engine
│   ├── compliance.py        # AML compliance
│   ├── ledger.py            # Privacy ledger
│   ├── offline.py           # Offline transfers
│   ├── zkp.py              # Zero-knowledge proofs
│   ├── cli.py              # Command-line interface
│   └── main.py             # System coordinator
├── tests/
│   └── demo_scenarios.py    # Comprehensive tests
├── requirements.txt         # Dependencies (none)
└── README.md              # This file
```

## System Components

### 1. Wallet System (`wallet.py`)
- **Purpose**: Digital wallet creation and management
- **Features**:
  - Cryptographic keypair generation
  - Token and voucher balance tracking
  - Transaction signing (simulated)
  - Pseudonymous identification

### 2. Token System (`token_system.py`)
- **Purpose**: Digital currency representation
- **Features**:
  - Euro-denominated tokens
  - Secure ownership transfer
  - Mock ECB issuance
  - Balance tracking

### 3. Voucher System (`voucher.py`)
- **Purpose**: Anonymity layer for transactions
- **Features**:
  - AML Authority signatures (mock)
  - Value limits for privacy
  - One-time use vouchers
  - Verification system

### 4. Transaction Engine (`transaction.py`)
- **Purpose**: Core transfer logic
- **Features**:
  - Ownership verification
  - Voucher redemption
  - AML routing
  - Ledger logging

### 5. Compliance System (`compliance.py`)
- **Purpose**: AML monitoring and reporting
- **Features**:
  - Risk scoring algorithms
  - Transaction flagging
  - Authority escalation
  - Regulatory reporting

### 6. Privacy Ledger (`ledger.py`)
- **Purpose**: Audit trail with privacy
- **Features**:
  - Pseudonymous entries
  - Anonymous/non-anonymous tracking
  - AML-flagged transactions
  - Export capabilities

### 7. Offline System (`offline.py`)
- **Purpose**: Peer-to-peer transfers
- **Features**:
  - Dual signature requirements
  - Local transaction storage
  - Ledger synchronization
  - Cash-like behavior

### 8. ZKP System (`zkp.py`)
- **Purpose**: Privacy verification
- **Features**:
  - Range proofs
  - Equality proofs
  - Membership proofs
  - Mock cryptographic verification

## CLI Commands

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
ledger query <params>       # Query ledger
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

## Privacy Features

### Pseudonymity
- Wallets use UUIDs for identification
- Public keys are cryptographic hashes
- No real-world identity linkage

### Anonymity
- Vouchers enable anonymous transactions
- AML Authority approval required
- Value limits prevent abuse

### Audit Trail
- Privacy-preserving ledger
- Distinguishes anonymous/non-anonymous
- AML-compliant reporting

### Offline Capability
- Peer-to-peer transfers
- No immediate ledger access
- Dual signature security

## Compliance Features

### AML Monitoring
- High-value transaction flagging (>€100)
- Anonymous transaction monitoring
- Risk scoring algorithms
- Authority escalation

### Regulatory Reporting
- AML registry entries
- Export capabilities
- Audit trail maintenance
- Compliance statistics

## Testing

Run comprehensive tests:
```bash
python3 tests/demo_scenarios.py
```

Test scenarios include:
- Wallet creation and management
- Token issuance and transfer
- Voucher system functionality
- Anonymous and regular transfers
- Offline transaction handling
- Compliance monitoring
- Ledger privacy features
- ZKP system verification
- Comprehensive system integration

## Data Storage

### File-Based Storage
- **Primary**: In-memory during runtime
- **Persistence**: JSON files for export
- **Ledger**: `privacy_ledger.json`
- **Exports**: Timestamped JSON files

### No Database Required
- Uses Python standard library only
- JSON-based data serialization
- File-based persistence
- No external dependencies

## Technical Implementation

### Cryptography (Simulated)
- SHA-256 hashing for signatures
- UUID generation for identifiers
- Mock keypair generation
- Simulated ZKP algorithms

### Data Structures
- Dataclasses for type safety
- Enums for status tracking
- Dictionaries for storage
- JSON for serialization

### Error Handling
- Comprehensive validation
- Graceful error messages
- Transaction rollback
- System integrity checks

## Use Cases

### 1. Digital Currency Research
- Privacy-preserving transactions
- Regulatory compliance
- Offline capabilities
- Cryptographic verification

### 2. AML Compliance Testing
- Risk scoring validation
- Transaction monitoring
- Authority escalation
- Audit trail verification

### 3. Privacy Technology Education
- Zero-knowledge proofs
- Anonymous transactions
- Pseudonymous systems
- Cryptographic concepts

### 4. Regulatory Framework Development
- Compliance rule testing
- Reporting mechanism validation
- Privacy vs. transparency balance
- Authority notification systems

## Future Enhancements

### Planned Features
- Real cryptographic signatures
- Blockchain integration
- Multi-currency support
- Advanced ZKP implementations
- Network synchronization
- Mobile wallet support
- Regulatory API integration
- Advanced AML algorithms

### Research Areas
- Privacy-preserving smart contracts
- Advanced zero-knowledge proofs
- Decentralized identity systems
- Cross-border compliance
- Quantum-resistant cryptography

## License

This project is for educational and research purposes. Please ensure compliance with local regulations when implementing privacy-preserving financial systems.

## Contributing

Contributions are welcome! Please ensure:
- Code follows Python standards
- Tests pass for new features
- Documentation is updated
- Privacy and security are maintained

## Support

For questions or issues:
1. Check the test scenarios
2. Review the CLI help
3. Examine the code documentation
4. Run the comprehensive demo

---

** Euromask** - Balancing privacy with compliance in digital currency systems.