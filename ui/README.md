# Privacy Network System - Web UI

A modern, interactive web interface for the Privacy Network System (PNS) that provides a visual way to interact with all system functionalities.

## Features

### 🎯 **Dashboard**
- Real-time system status overview
- Quick action buttons for common operations
- Live statistics and progress indicators
- Recent activity feed

### 👛 **Wallet Management**
- Create new wallets with cryptographic keypairs
- View wallet balances and details
- Copy wallet IDs and keys
- Secure key management with visibility toggles

### 🪙 **Token System**
- Issue new digital currency tokens
- Assign tokens to specific wallets
- View token distribution and ownership
- Track total system value

### 🎫 **Voucher System**
- Issue anonymity vouchers with value limits
- Assign vouchers to specific wallets
- Track voucher usage and availability
- Privacy-enabling transaction vouchers

### 💸 **Transaction Engine**
- Execute regular and anonymous transfers
- Real-time transaction status updates
- AML compliance monitoring
- Transaction history and audit trail

### 📱 **Offline Transactions**
- Create peer-to-peer offline transfers
- Dual-signature verification system
- Offline transaction synchronization
- P2P cash-like functionality

### 🛡️ **Compliance & AML**
- Real-time transaction monitoring
- Risk scoring and flagging
- AML report generation
- Regulatory compliance tracking

### 📚 **Privacy Ledger**
- Privacy-preserving audit trail
- Anonymous vs non-anonymous transaction tracking
- Export capabilities for regulatory reporting
- Volume analysis and statistics

### 🔐 **Zero-Knowledge Proofs**
- Generate various types of ZKP proofs
- Range proofs, equality proofs, membership proofs
- Privacy-preserving verifications
- Proof verification and validation

### 🎭 **Interactive Demo**
- Complete system demonstration
- Step-by-step progress tracking
- Real-time result visualization
- Educational showcase of all features

## Installation

### Prerequisites
- Python 3.8 or higher
- The main PNS system must be installed and working

### Setup

1. **Install UI Dependencies**
   ```bash
   cd ui
   pip install -r requirements.txt
   ```

2. **Start the Web Server**
   ```bash
   python app.py
   ```

3. **Access the Interface**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Getting Started

1. **Dashboard Overview**
   - Visit the main dashboard to see system status
   - Use quick action buttons for common tasks
   - Monitor real-time statistics

2. **Create Your First Wallet**
   - Click "Create New Wallet" button
   - View the generated wallet ID and keys
   - Copy the wallet ID for future use

3. **Issue Tokens**
   - Select a wallet to receive tokens
   - Specify the token value in euros
   - Confirm the issuance

4. **Run the Demo**
   - Visit the Demo page
   - Click "Run Complete Demo" to see all features
   - Watch the progress and results in real-time

### Key Features

#### Real-time Updates
- WebSocket connections provide live updates
- Toast notifications for all actions
- Auto-refreshing status indicators

#### Interactive Modals
- Create wallets, tokens, and vouchers through modals
- Form validation and error handling
- Success/error feedback

#### Responsive Design
- Mobile-friendly interface
- Modern Bootstrap 5 styling
- Smooth animations and transitions

#### Security Features
- Secure key management
- Password-protected private keys
- Copy-to-clipboard functionality

## API Endpoints

The web UI communicates with the PNS system through REST API endpoints:

- `GET /api/status` - Get system status
- `POST /api/wallets` - Create new wallet
- `POST /api/tokens` - Issue new token
- `POST /api/vouchers` - Issue new voucher
- `POST /api/transactions` - Execute transaction
- `POST /api/offline` - Create offline transaction
- `POST /api/zkp` - Generate ZKP proof
- `POST /api/demo` - Run system demo
- `POST /api/export` - Export system data

## WebSocket Events

Real-time updates are provided through WebSocket events:

- `wallet_created` - New wallet created
- `token_issued` - New token issued
- `voucher_issued` - New voucher issued
- `transaction_executed` - Transaction completed
- `offline_transaction_created` - Offline transaction created
- `offline_transaction_signed` - Offline transaction signed
- `zkp_generated` - ZKP proof generated
- `demo_completed` - Demo finished
- `export_completed` - Export finished

## File Structure

```
ui/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Dashboard page
    ├── wallets.html      # Wallet management
    ├── tokens.html       # Token management
    ├── vouchers.html     # Voucher management
    ├── transactions.html # Transaction management
    ├── offline.html      # Offline transactions
    ├── compliance.html   # AML compliance
    ├── ledger.html       # Privacy ledger
    ├── zkp.html          # Zero-knowledge proofs
    ├── demo.html         # Interactive demo
    └── export.html       # Data export
```

## Customization

### Styling
The UI uses Bootstrap 5 with custom CSS variables for easy theming:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

### Adding New Features
1. Create new route in `app.py`
2. Add corresponding template in `templates/`
3. Update navigation in `base.html`
4. Add WebSocket events if needed

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure the main PNS system is properly installed
   - Check that `src/` directory is accessible

2. **Port Already in Use**
   - Change the port in `app.py` line 277
   - Or kill the process using port 5000

3. **WebSocket Connection Issues**
   - Check browser console for errors
   - Ensure no firewall blocking WebSocket connections

4. **Template Errors**
   - Verify all template files are in `templates/` directory
   - Check for syntax errors in Jinja2 templates

### Debug Mode
Run the app in debug mode for detailed error messages:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

## Security Notes

- The web UI is for demonstration purposes
- Private keys are displayed in plain text (for demo only)
- In production, implement proper key management
- Add authentication and authorization
- Use HTTPS in production environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This web UI is part of the Privacy Network System and follows the same license terms. 