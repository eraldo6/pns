"""
Offline Transfer Simulation
Handles peer-to-peer transactions without immediate ledger access
"""

import uuid
import hashlib
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OfflineStatus(Enum):
    """Offline transaction status"""
    PENDING = "pending"
    SIGNED = "signed"
    SYNCED = "synced"
    FAILED = "failed"


@dataclass
class OfflineTransaction:
    """Offline transaction between peers"""
    offline_id: str
    sender_wallet_id: str
    receiver_wallet_id: str
    token_id: str
    value: int
    sender_signature: Optional[str] = None
    receiver_signature: Optional[str] = None
    status: OfflineStatus = OfflineStatus.PENDING
    created_timestamp: Optional[str] = None
    synced_timestamp: Optional[str] = None
    voucher_id: Optional[str] = None
    is_anonymous: bool = False
    
    def __post_init__(self):
        """Initialize offline transaction"""
        if not self.created_timestamp:
            self.created_timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'offline_id': self.offline_id,
            'sender_wallet_id': self.sender_wallet_id,
            'receiver_wallet_id': self.receiver_wallet_id,
            'token_id': self.token_id,
            'value': self.value,
            'sender_signature': self.sender_signature,
            'receiver_signature': self.receiver_signature,
            'status': self.status.value,
            'created_timestamp': self.created_timestamp,
            'synced_timestamp': self.synced_timestamp,
            'voucher_id': self.voucher_id,
            'is_anonymous': self.is_anonymous
        }


class OfflineManager:
    """Manages offline transactions and synchronization"""
    
    def __init__(self):
        self.offline_transactions: Dict[str, OfflineTransaction] = {}
        self.wallet_manager = None
        self.token_manager = None
        self.voucher_manager = None
        self.ledger_manager = None
    
    def set_managers(self, wallet_manager, token_manager, voucher_manager, ledger_manager):
        """Set references to managers"""
        self.wallet_manager = wallet_manager
        self.token_manager = token_manager
        self.voucher_manager = voucher_manager
        self.ledger_manager = ledger_manager
    
    def create_offline_transaction(self, sender_wallet_id: str, receiver_wallet_id: str,
                                 token_id: str, voucher_id: Optional[str] = None) -> OfflineTransaction:
        """Create a new offline transaction"""
        
        # Validate inputs
        if not all([sender_wallet_id, receiver_wallet_id, token_id]):
            raise ValueError("Sender, receiver, and token ID are required")
        
        if sender_wallet_id == receiver_wallet_id:
            raise ValueError("Sender and receiver cannot be the same")
        
        # Check if wallets exist
        if not self.wallet_manager:
            raise ValueError("Wallet manager not set")
        
        if not (self.wallet_manager.wallet_exists(sender_wallet_id) and 
                self.wallet_manager.wallet_exists(receiver_wallet_id)):
            raise ValueError("One or both wallets do not exist")
        
        # Check if token exists and is owned by sender
        if not self.token_manager:
            raise ValueError("Token manager not set")
        
        token = self.token_manager.get_token(token_id)
        if not token:
            raise ValueError(f"Token {token_id} does not exist")
        
        if token.owner_wallet_id != sender_wallet_id:
            raise ValueError(f"Sender does not own token {token_id}")
        
        # Check voucher if provided
        is_anonymous = False
        if voucher_id:
            if not self.voucher_manager:
                raise ValueError("Voucher manager not set")
            
            voucher = self.voucher_manager.get_voucher(voucher_id)
            if not voucher:
                raise ValueError(f"Voucher {voucher_id} does not exist")
            
            if voucher.issued_to_wallet_id != sender_wallet_id:
                raise ValueError(f"Voucher {voucher_id} does not belong to sender")
            
            if not voucher.can_be_used_for_value(token.value):
                raise ValueError(f"Voucher {voucher_id} cannot be used for value €{token.value}")
            
            is_anonymous = True
        
        # Create offline transaction
        offline_id = str(uuid.uuid4())
        offline_tx = OfflineTransaction(
            offline_id=offline_id,
            sender_wallet_id=sender_wallet_id,
            receiver_wallet_id=receiver_wallet_id,
            token_id=token_id,
            value=token.value,
            voucher_id=voucher_id,
            is_anonymous=is_anonymous
        )
        
        self.offline_transactions[offline_id] = offline_tx
        return offline_tx
    
    def sign_offline_transaction(self, offline_id: str, wallet_id: str, signature: str) -> bool:
        """Sign an offline transaction (simulated dual signature)"""
        offline_tx = self.offline_transactions.get(offline_id)
        if not offline_tx:
            return False
        
        # Validate signature (simulated)
        if not self._verify_offline_signature(offline_tx, wallet_id, signature):
            return False
        
        # Apply signature based on wallet role
        if wallet_id == offline_tx.sender_wallet_id:
            offline_tx.sender_signature = signature
        elif wallet_id == offline_tx.receiver_wallet_id:
            offline_tx.receiver_signature = signature
        else:
            return False
        
        # Check if both signatures are present
        if offline_tx.sender_signature and offline_tx.receiver_signature:
            offline_tx.status = OfflineStatus.SIGNED
        
        return True
    
    def _verify_offline_signature(self, offline_tx: OfflineTransaction, wallet_id: str, signature: str) -> bool:
        """Verify offline transaction signature (simulated)"""
        if not self.wallet_manager:
            return False
        
        wallet = self.wallet_manager.get_wallet(wallet_id)
        if not wallet:
            return False
        
        # Create transaction data for signature verification
        tx_data = {
            'offline_id': offline_tx.offline_id,
            'sender_wallet_id': offline_tx.sender_wallet_id,
            'receiver_wallet_id': offline_tx.receiver_wallet_id,
            'token_id': offline_tx.token_id,
            'value': offline_tx.value,
            'voucher_id': offline_tx.voucher_id,
            'is_anonymous': offline_tx.is_anonymous
        }
        
        # Simulate signature verification
        expected_signature = wallet.sign_transaction(tx_data)
        return signature == expected_signature
    
    def sync_with_ledger(self, offline_id: str) -> bool:
        """Synchronize offline transaction with the main ledger"""
        offline_tx = self.offline_transactions.get(offline_id)
        if not offline_tx:
            return False
        
        # Check if transaction is fully signed
        if offline_tx.status != OfflineStatus.SIGNED:
            return False
        
        try:
            # Transfer token ownership
            if not self.token_manager:
                return False
            
            transfer_success = self.token_manager.transfer_token(
                offline_tx.token_id, 
                offline_tx.sender_wallet_id, 
                offline_tx.receiver_wallet_id
            )
            
            if not transfer_success:
                offline_tx.status = OfflineStatus.FAILED
                return False
            
            # Redeem voucher if used
            if offline_tx.voucher_id and self.voucher_manager:
                voucher_redeemed = self.voucher_manager.redeem_voucher(
                    offline_tx.voucher_id, 
                    offline_tx.offline_id, 
                    offline_tx.value
                )
                if not voucher_redeemed:
                    offline_tx.status = OfflineStatus.FAILED
                    return False
            
            # Create ledger entry
            if self.ledger_manager:
                # Create a transaction-like object for ledger storage
                class MockTransaction:
                    def __init__(self, offline_tx):
                        self.transaction_id = offline_tx.offline_id
                        self.sender_wallet_id = offline_tx.sender_wallet_id
                        self.receiver_wallet_id = offline_tx.receiver_wallet_id
                        self.token_id = offline_tx.token_id
                        self.voucher_id = offline_tx.voucher_id
                        self.is_anonymous = offline_tx.is_anonymous
                        self.aml_flagged = False
                        self.aml_reason = None
                        self.timestamp = offline_tx.created_timestamp
                        self.status = type('Status', (), {'value': 'completed'})()
                
                mock_tx = MockTransaction(offline_tx)
                self.ledger_manager.store_transaction(mock_tx)
            
            # Mark as synced
            offline_tx.status = OfflineStatus.SYNCED
            offline_tx.synced_timestamp = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            offline_tx.status = OfflineStatus.FAILED
            return False
    
    def get_offline_transaction(self, offline_id: str) -> Optional[OfflineTransaction]:
        """Get offline transaction by ID"""
        return self.offline_transactions.get(offline_id)
    
    def get_pending_offline_transactions(self) -> List[OfflineTransaction]:
        """Get all pending offline transactions"""
        return [tx for tx in self.offline_transactions.values() 
                if tx.status == OfflineStatus.PENDING]
    
    def get_signed_offline_transactions(self) -> List[OfflineTransaction]:
        """Get all signed offline transactions ready for sync"""
        return [tx for tx in self.offline_transactions.values() 
                if tx.status == OfflineStatus.SIGNED]
    
    def get_synced_offline_transactions(self) -> List[OfflineTransaction]:
        """Get all synced offline transactions"""
        return [tx for tx in self.offline_transactions.values() 
                if tx.status == OfflineStatus.SYNCED]
    
    def get_failed_offline_transactions(self) -> List[OfflineTransaction]:
        """Get all failed offline transactions"""
        return [tx for tx in self.offline_transactions.values() 
                if tx.status == OfflineStatus.FAILED]
    
    def get_offline_transactions_by_wallet(self, wallet_id: str) -> List[OfflineTransaction]:
        """Get all offline transactions involving a wallet"""
        return [tx for tx in self.offline_transactions.values() 
                if tx.sender_wallet_id == wallet_id or tx.receiver_wallet_id == wallet_id]
    
    def list_all_offline_transactions(self) -> List[OfflineTransaction]:
        """List all offline transactions"""
        return list(self.offline_transactions.values())
    
    def get_offline_statistics(self) -> Dict:
        """Get offline transaction statistics"""
        total_transactions = len(self.offline_transactions)
        pending_transactions = self.get_pending_offline_transactions()
        signed_transactions = self.get_signed_offline_transactions()
        synced_transactions = self.get_synced_offline_transactions()
        failed_transactions = self.get_failed_offline_transactions()
        
        return {
            'total_offline_transactions': total_transactions,
            'pending_transactions': len(pending_transactions),
            'signed_transactions': len(signed_transactions),
            'synced_transactions': len(synced_transactions),
            'failed_transactions': len(failed_transactions),
            'sync_rate': (len(synced_transactions) / total_transactions * 100) if total_transactions > 0 else 0,
            'failure_rate': (len(failed_transactions) / total_transactions * 100) if total_transactions > 0 else 0
        }
    
    def export_offline_transactions(self, filename: str = None) -> str:
        """Export offline transactions to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"offline_transactions_{timestamp}.json"
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_transactions': len(self.offline_transactions),
            'statistics': self.get_offline_statistics(),
            'transactions': [tx.to_dict() for tx in self.offline_transactions.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename 