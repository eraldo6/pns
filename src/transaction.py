"""
Transaction Engine Implementation
Handles token transfers with ownership verification and AML routing
"""

import uuid
import hashlib
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionStatus(Enum):
    """Transaction status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Transaction:
    """Digital transaction between wallets"""
    transaction_id: str
    sender_wallet_id: str
    receiver_wallet_id: str
    token_id: str
    voucher_id: Optional[str] = None
    is_anonymous: bool = False
    status: TransactionStatus = TransactionStatus.PENDING
    timestamp: Optional[str] = None
    aml_flagged: bool = False
    aml_reason: Optional[str] = None
    signature: Optional[str] = None
    
    def __post_init__(self):
        """Initialize transaction after creation"""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'sender_wallet_id': self.sender_wallet_id,
            'receiver_wallet_id': self.receiver_wallet_id,
            'token_id': self.token_id,
            'voucher_id': self.voucher_id,
            'is_anonymous': self.is_anonymous,
            'status': self.status.value,
            'timestamp': self.timestamp,
            'aml_flagged': self.aml_flagged,
            'aml_reason': self.aml_reason,
            'signature': self.signature
        }


class TransactionEngine:
    """Engine for executing token transfers"""
    
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.wallet_manager = None
        self.token_manager = None
        self.voucher_manager = None
        self.compliance_manager = None
        self.ledger_manager = None
    
    def set_managers(self, wallet_manager, token_manager, voucher_manager, 
                    compliance_manager, ledger_manager):
        """Set references to all managers"""
        self.wallet_manager = wallet_manager
        self.token_manager = token_manager
        self.voucher_manager = voucher_manager
        self.compliance_manager = compliance_manager
        self.ledger_manager = ledger_manager
    
    def execute_transfer(self, sender_wallet_id: str, receiver_wallet_id: str, 
                        token_id: str, voucher_id: Optional[str] = None) -> Transaction:
        """Execute a token transfer between wallets"""
        
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
        
        # Determine if transaction is anonymous
        is_anonymous = False
        if voucher_id:
            if not self.voucher_manager:
                raise ValueError("Voucher manager not set")
            
            voucher = self.voucher_manager.get_voucher(voucher_id)
            if not voucher:
                raise ValueError(f"Voucher {voucher_id} does not exist")
            
            # Verify voucher belongs to sender
            if voucher.issued_to_wallet_id != sender_wallet_id:
                raise ValueError(f"Voucher {voucher_id} does not belong to sender")
            
            # Check if voucher can be used for this transaction
            if not voucher.can_be_used_for_value(token.value):
                raise ValueError(f"Voucher {voucher_id} cannot be used for value €{token.value}")
            
            is_anonymous = True
        
        # Create transaction
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            sender_wallet_id=sender_wallet_id,
            receiver_wallet_id=receiver_wallet_id,
            token_id=token_id,
            voucher_id=voucher_id,
            is_anonymous=is_anonymous
        )
        
        # Perform compliance check
        if self.compliance_manager:
            compliance_result = self.compliance_manager.check_transaction(transaction, token)
            transaction.aml_flagged = compliance_result.status.value == "flagged"
            transaction.aml_reason = compliance_result.reason
        
        # Execute the transfer
        try:
            # Transfer token ownership
            transfer_success = self.token_manager.transfer_token(
                token_id, sender_wallet_id, receiver_wallet_id
            )
            
            if not transfer_success:
                transaction.status = TransactionStatus.FAILED
                raise ValueError("Token transfer failed")
            
            # Redeem voucher if used
            if voucher_id and self.voucher_manager:
                voucher_redeemed = self.voucher_manager.redeem_voucher(
                    voucher_id, transaction_id, token.value
                )
                if not voucher_redeemed:
                    transaction.status = TransactionStatus.FAILED
                    raise ValueError("Voucher redemption failed")
            
            # Sign transaction (simulated)
            if self.wallet_manager:
                sender_wallet = self.wallet_manager.get_wallet(sender_wallet_id)
                if sender_wallet:
                    transaction.signature = sender_wallet.sign_transaction(transaction.to_dict())
            
            # Mark transaction as completed
            transaction.status = TransactionStatus.COMPLETED
            
            # Store in ledger
            if self.ledger_manager:
                self.ledger_manager.store_transaction(transaction)
            
            # Store transaction
            self.transactions[transaction_id] = transaction
            
            return transaction
            
        except Exception as e:
            transaction.status = TransactionStatus.FAILED
            raise e
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        return self.transactions.get(transaction_id)
    
    def get_transactions_by_wallet(self, wallet_id: str) -> List[Transaction]:
        """Get all transactions involving a wallet"""
        return [tx for tx in self.transactions.values() 
                if tx.sender_wallet_id == wallet_id or tx.receiver_wallet_id == wallet_id]
    
    def get_anonymous_transactions(self) -> List[Transaction]:
        """Get all anonymous transactions"""
        return [tx for tx in self.transactions.values() if tx.is_anonymous]
    
    def get_non_anonymous_transactions(self) -> List[Transaction]:
        """Get all non-anonymous transactions"""
        return [tx for tx in self.transactions.values() if not tx.is_anonymous]
    
    def get_aml_flagged_transactions(self) -> List[Transaction]:
        """Get all AML-flagged transactions"""
        return [tx for tx in self.transactions.values() if tx.aml_flagged]
    
    def get_completed_transactions(self) -> List[Transaction]:
        """Get all completed transactions"""
        return [tx for tx in self.transactions.values() if tx.status == TransactionStatus.COMPLETED]
    
    def get_failed_transactions(self) -> List[Transaction]:
        """Get all failed transactions"""
        return [tx for tx in self.transactions.values() if tx.status == TransactionStatus.FAILED]
    
    def list_all_transactions(self) -> List[Transaction]:
        """List all transactions"""
        return list(self.transactions.values())
    
    def get_transaction_statistics(self) -> Dict:
        """Get transaction statistics"""
        total_transactions = len(self.transactions)
        anonymous_transactions = self.get_anonymous_transactions()
        non_anonymous_transactions = self.get_non_anonymous_transactions()
        aml_flagged_transactions = self.get_aml_flagged_transactions()
        completed_transactions = self.get_completed_transactions()
        failed_transactions = self.get_failed_transactions()
        
        return {
            'total_transactions': total_transactions,
            'anonymous_transactions': len(anonymous_transactions),
            'non_anonymous_transactions': len(non_anonymous_transactions),
            'aml_flagged_transactions': len(aml_flagged_transactions),
            'completed_transactions': len(completed_transactions),
            'failed_transactions': len(failed_transactions),
            'success_rate': (len(completed_transactions) / total_transactions * 100) if total_transactions > 0 else 0,
            'anonymous_percentage': (len(anonymous_transactions) / total_transactions * 100) if total_transactions > 0 else 0
        }
    
    def verify_transaction_signature(self, transaction_id: str) -> bool:
        """Verify transaction signature"""
        transaction = self.get_transaction(transaction_id)
        if not transaction or not transaction.signature:
            return False
        
        if not self.wallet_manager:
            return False
        
        sender_wallet = self.wallet_manager.get_wallet(transaction.sender_wallet_id)
        if not sender_wallet:
            return False
        
        # Create transaction data without signature for verification
        transaction_data = transaction.to_dict()
        transaction_data.pop('signature', None)
        
        return sender_wallet.verify_signature(transaction_data, transaction.signature) 