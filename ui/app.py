#!/usr/bin/env python3
"""
Euromask - Web UI
A modern web interface for the PNS digital currency system
"""

import sys
import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import threading
import time

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import PNS components
from main import PrivacyNetworkSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pns-secret-key-2025'
socketio = SocketIO(app)

# Global PNS system instance
pns_system = None

def initialize_pns():
    """Initialize the PNS system"""
    global pns_system
    pns_system = PrivacyNetworkSystem()
    return pns_system

@app.route('/')
def index():
    """Main dashboard page"""
    if pns_system is None:
        initialize_pns()
    
    status = pns_system.get_system_status()
    return render_template('index.html', status=status)

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    if pns_system is None:
        initialize_pns()
    
    status = pns_system.get_system_status()
    return jsonify(status)

@app.route('/wallets')
def wallets():
    """Wallet management page"""
    if pns_system is None:
        initialize_pns()
    
    wallets = pns_system.wallet_manager.list_wallets()
    return render_template('wallets.html', wallets=wallets)

@app.route('/api/wallets', methods=['POST'])
def create_wallet():
    """API endpoint to create a new wallet"""
    try:
        wallet = pns_system.wallet_manager.create_wallet()
        socketio.emit('wallet_created', {
            'wallet_id': wallet.wallet_id,
            'public_key': wallet.public_key[:20] + '...',
            'balance': wallet.token_balance
        })
        return jsonify({
            'success': True,
            'wallet': {
                'wallet_id': wallet.wallet_id,
                'public_key': wallet.public_key,
                'private_key': wallet.private_key,
                'token_balance': wallet.token_balance,
                'voucher_balance': wallet.voucher_balance
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/tokens')
def tokens():
    """Token management page"""
    if pns_system is None:
        initialize_pns()
    
    tokens = pns_system.token_manager.list_all_tokens()
    wallets = pns_system.wallet_manager.list_wallets()
    return render_template('tokens.html', tokens=tokens, wallets=wallets)

@app.route('/api/tokens', methods=['POST'])
def issue_token():
    """API endpoint to issue a new token"""
    try:
        data = request.get_json()
        value = float(data.get('value', 100))
        owner_wallet_id = data.get('owner_wallet_id')
        
        token = pns_system.token_manager.issue_token(value, owner_wallet_id)
        socketio.emit('token_issued', {
            'token_id': token.token_id,
            'value': token.value,
            'owner_wallet_id': token.owner_wallet_id
        })
        return jsonify({
            'success': True,
            'token': {
                'token_id': token.token_id,
                'value': token.value,
                'owner_wallet_id': token.owner_wallet_id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/vouchers')
def vouchers():
    """Voucher management page"""
    if pns_system is None:
        initialize_pns()
    
    vouchers = pns_system.voucher_manager.list_all_vouchers()
    wallets = pns_system.wallet_manager.list_wallets()
    return render_template('vouchers.html', vouchers=vouchers, wallets=wallets)

@app.route('/api/vouchers', methods=['POST'])
def issue_voucher():
    """API endpoint to issue a new voucher"""
    try:
        data = request.get_json()
        value_limit = float(data.get('value_limit', 50))
        issued_to_wallet_id = data.get('issued_to_wallet_id')
        
        # Issue voucher with correct parameter order
        voucher = pns_system.voucher_manager.issue_voucher(issued_to_wallet_id, value_limit)
        socketio.emit('voucher_issued', {
            'voucher_id': voucher.voucher_id,
            'value_limit': voucher.value_limit,
            'issued_to_wallet_id': voucher.issued_to_wallet_id
        })
        return jsonify({
            'success': True,
            'voucher': {
                'voucher_id': voucher.voucher_id,
                'value_limit': voucher.value_limit,
                'issued_to_wallet_id': voucher.issued_to_wallet_id,
                'is_used': voucher.is_used
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/transactions')
def transactions():
    """Transaction management page"""
    if pns_system is None:
        initialize_pns()
    
    # Get recent transactions from ledger (handle missing method)
    try:
        ledger_entries = pns_system.ledger_manager.get_recent_entries(20)
    except AttributeError:
        # If method doesn't exist, use empty list
        ledger_entries = []
    
    wallets = pns_system.wallet_manager.list_wallets()
    tokens = pns_system.token_manager.list_all_tokens()
    vouchers = pns_system.voucher_manager.list_all_vouchers()
    
    return render_template('transactions.html', 
                         transactions=ledger_entries,
                         wallets=wallets,
                         tokens=tokens,
                         vouchers=vouchers)

@app.route('/api/transactions', methods=['POST'])
def execute_transaction():
    """API endpoint to execute a transaction"""
    try:
        data = request.get_json()
        sender_wallet_id = data.get('sender_wallet_id')
        receiver_wallet_id = data.get('receiver_wallet_id')
        token_id = data.get('token_id')
        voucher_id = data.get('voucher_id')
        is_anonymous = data.get('is_anonymous', False)
        
        transaction = pns_system.transaction_engine.execute_transfer(
            sender_wallet_id, receiver_wallet_id, token_id, voucher_id, is_anonymous
        )
        
        socketio.emit('transaction_executed', {
            'transaction_id': transaction.transaction_id,
            'sender_wallet_id': transaction.sender_wallet_id,
            'receiver_wallet_id': transaction.receiver_wallet_id,
            'is_anonymous': transaction.is_anonymous,
            'status': transaction.status.value,
            'aml_flagged': transaction.aml_flagged
        })
        
        return jsonify({
            'success': True,
            'transaction': {
                'transaction_id': transaction.transaction_id,
                'sender_wallet_id': transaction.sender_wallet_id,
                'receiver_wallet_id': transaction.receiver_wallet_id,
                'token_id': transaction.token_id,
                'voucher_id': transaction.voucher_id,
                'is_anonymous': transaction.is_anonymous,
                'status': transaction.status.value,
                'aml_flagged': transaction.aml_flagged,
                'timestamp': transaction.timestamp
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/offline')
def offline():
    """Offline transaction page"""
    if pns_system is None:
        initialize_pns()
    
    # Get offline transactions (handle missing method)
    try:
        offline_transactions = pns_system.offline_manager.list_offline_transactions()
    except AttributeError:
        # If method doesn't exist, use empty list
        offline_transactions = []
    
    wallets = pns_system.wallet_manager.list_wallets()
    tokens = pns_system.token_manager.list_all_tokens()
    vouchers = pns_system.voucher_manager.list_all_vouchers()
    
    return render_template('offline.html', 
                         offline_transactions=offline_transactions,
                         wallets=wallets,
                         tokens=tokens,
                         vouchers=vouchers)

@app.route('/api/offline', methods=['POST'])
def create_offline_transaction():
    """API endpoint to create an offline transaction"""
    try:
        data = request.get_json()
        sender_wallet_id = data.get('sender_wallet_id')
        receiver_wallet_id = data.get('receiver_wallet_id')
        token_id = data.get('token_id')
        voucher_id = data.get('voucher_id')
        is_anonymous = data.get('is_anonymous', False)
        
        offline_tx = pns_system.offline_manager.create_offline_transaction(
            sender_wallet_id, receiver_wallet_id, token_id, voucher_id, is_anonymous
        )
        
        socketio.emit('offline_transaction_created', {
            'offline_id': offline_tx.offline_id,
            'sender_wallet_id': offline_tx.sender_wallet_id,
            'receiver_wallet_id': offline_tx.receiver_wallet_id,
            'status': offline_tx.status
        })
        
        return jsonify({
            'success': True,
            'offline_transaction': {
                'offline_id': offline_tx.offline_id,
                'sender_wallet_id': offline_tx.sender_wallet_id,
                'receiver_wallet_id': offline_tx.receiver_wallet_id,
                'token_id': offline_tx.token_id,
                'voucher_id': offline_tx.voucher_id,
                'is_anonymous': offline_tx.is_anonymous,
                'status': offline_tx.status,
                'created_at': offline_tx.created_at
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/offline/<offline_id>/sign', methods=['POST'])
def sign_offline_transaction(offline_id):
    """API endpoint to sign an offline transaction"""
    try:
        data = request.get_json()
        wallet_id = data.get('wallet_id')
        signature = data.get('signature')
        
        success = pns_system.offline_manager.sign_offline_transaction(
            offline_id, wallet_id, signature
        )
        
        if success:
            socketio.emit('offline_transaction_signed', {
                'offline_id': offline_id,
                'wallet_id': wallet_id
            })
        
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/compliance')
def compliance():
    """Compliance and AML page"""
    if pns_system is None:
        initialize_pns()
    
    # Get AML entries (handle missing method)
    try:
        aml_entries = pns_system.compliance_manager.get_aml_entries()
    except AttributeError:
        # If method doesn't exist, use empty list
        aml_entries = []
    
    return render_template('compliance.html', aml_entries=aml_entries)

@app.route('/ledger')
def ledger():
    """Privacy ledger page"""
    if pns_system is None:
        initialize_pns()
    
    # Get ledger statistics (handle missing methods)
    try:
        stats = pns_system.ledger_manager.get_ledger_statistics()
    except AttributeError:
        # If method doesn't exist, use default stats
        stats = {
            'total_entries': 0,
            'anonymous_entries': 0,
            'non_anonymous_entries': 0,
            'aml_flagged_entries': 0
        }
    
    try:
        recent_entries = pns_system.ledger_manager.get_recent_entries(50)
    except AttributeError:
        # If method doesn't exist, use empty list
        recent_entries = []
    
    return render_template('ledger.html', 
                         statistics=stats,
                         entries=recent_entries)

@app.route('/zkp')
def zkp():
    """Zero-knowledge proofs page"""
    if pns_system is None:
        initialize_pns()
    
    # Get ZKP proofs (handle missing method)
    try:
        proofs = pns_system.zkp_manager.list_all_proofs()
    except AttributeError:
        # If method doesn't exist, use empty list
        proofs = []
    
    return render_template('zkp.html', proofs=proofs)

@app.route('/api/zkp', methods=['POST'])
def generate_zkp():
    """API endpoint to generate a ZKP"""
    try:
        data = request.get_json()
        proof_type = data.get('proof_type', 'range_proof')
        statement = data.get('statement', 'Prove value is between 0 and 1000')
        private_inputs = data.get('private_inputs', {})
        public_inputs = data.get('public_inputs', {})
        
        proof = pns_system.zkp_manager.generate_proof(
            proof_type, statement, private_inputs, public_inputs
        )
        
        socketio.emit('zkp_generated', {
            'proof_id': proof.proof_id,
            'proof_type': proof.proof_type,
            'statement': proof.statement
        })
        
        return jsonify({
            'success': True,
            'proof': {
                'proof_id': proof.proof_id,
                'proof_type': proof.proof_type,
                'statement': proof.statement,
                'proof_data': proof.proof_data,
                'verified': proof.verified,
                'created_at': proof.created_at
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/demo')
def demo():
    """Demo page"""
    return render_template('demo.html')

@app.route('/api/demo', methods=['POST'])
def run_demo():
    """API endpoint to run the demo"""
    try:
        # Run demo in background thread
        def run_demo_thread():
            try:
                pns_system.run_demo()
                socketio.emit('demo_completed', {'success': True})
            except Exception as e:
                socketio.emit('demo_completed', {'success': False, 'error': str(e)})
        
        thread = threading.Thread(target=run_demo_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Demo started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export')
def export():
    """Export page"""
    if pns_system is None:
        initialize_pns()
    
    return render_template('export.html')

@app.route('/api/export', methods=['POST'])
def export_data():
    """API endpoint to export system data"""
    try:
        export_files = pns_system.export_system_data()
        socketio.emit('export_completed', {
            'files': export_files
        })
        return jsonify({
            'success': True,
            'files': export_files
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'message': 'Connected to PNS Web UI'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Initialize PNS system
    initialize_pns()
    
    print("Euromask - Web UI")
    print("==================================")
    print("Starting web server...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Run the Flask app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True) 