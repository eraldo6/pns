"""
Voucher System Implementation
Handles anonymity vouchers for private transactions
"""

import uuid
import hashlib
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Voucher:
    """Anonymity voucher for private transactions"""
    voucher_id: str
    signature: str  # Issued by AMLAuthority (mock signed)
    value_limit: int  # Max allowed transaction value in euros
    issued_to_wallet_id: str
    issued_by: str = "AMLAuthority"
    issue_timestamp: Optional[str] = None
    is_used: bool = False
    used_in_transaction: Optional[str] = None
    
    def __post_init__(self):
        """Validate voucher after creation"""
        if not self.voucher_id or not self.signature or self.value_limit <= 0:
            raise ValueError("Voucher must have valid ID, signature, and positive value limit")
    
    def can_be_used_for_value(self, value: int) -> bool:
        """Check if voucher can be used for given transaction value"""
        return not self.is_used and value <= self.value_limit
    
    def mark_as_used(self, transaction_id: str) -> bool:
        """Mark voucher as used in a transaction"""
        if not self.is_used:
            self.is_used = True
            self.used_in_transaction = transaction_id
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert voucher to dictionary for serialization"""
        return {
            'voucher_id': self.voucher_id,
            'signature': self.signature,
            'value_limit': self.value_limit,
            'issued_to_wallet_id': self.issued_to_wallet_id,
            'issued_by': self.issued_by,
            'issue_timestamp': self.issue_timestamp,
            'is_used': self.is_used,
            'used_in_transaction': self.used_in_transaction
        }


class VoucherManager:
    """Manages voucher issuance, redemption, and tracking"""
    
    def __init__(self):
        self.vouchers: Dict[str, Voucher] = {}
        self.wallet_manager = None  # Will be set by main system
        self.aml_authority_private_key = "aml_authority_secret_key_123"  # Mock private key
    
    def set_wallet_manager(self, wallet_manager):
        """Set reference to wallet manager"""
        self.wallet_manager = wallet_manager
    
    def _generate_aml_signature(self, voucher_data: Dict) -> str:
        """Generate mock AML Authority signature"""
        data_str = json.dumps(voucher_data, sort_keys=True)
        signature = hashlib.sha256((data_str + self.aml_authority_private_key).encode()).hexdigest()
        return signature
    
    def issue_voucher(self, wallet_id: str, value_limit: int) -> Voucher:
        """Issue a voucher to a wallet (mock AML Authority)"""
        if not self.wallet_manager or not self.wallet_manager.wallet_exists(wallet_id):
            raise ValueError(f"Wallet {wallet_id} does not exist")
        
        voucher_id = str(uuid.uuid4())
        voucher_data = {
            'voucher_id': voucher_id,
            'value_limit': value_limit,
            'issued_to_wallet_id': wallet_id,
            'issued_by': 'AMLAuthority',
            'issue_timestamp': datetime.now().isoformat()
        }
        
        signature = self._generate_aml_signature(voucher_data)
        
        voucher = Voucher(
            voucher_id=voucher_id,
            signature=signature,
            value_limit=value_limit,
            issued_to_wallet_id=wallet_id,
            issue_timestamp=voucher_data['issue_timestamp']
        )
        
        self.vouchers[voucher_id] = voucher
        
        # Add voucher to wallet
        wallet = self.wallet_manager.get_wallet(wallet_id)
        if wallet:
            wallet.add_voucher(1)
        
        return voucher
    
    def get_voucher(self, voucher_id: str) -> Optional[Voucher]:
        """Retrieve voucher by ID"""
        return self.vouchers.get(voucher_id)
    
    def redeem_voucher(self, voucher_id: str, transaction_id: str, transaction_value: int) -> bool:
        """Redeem voucher for a transaction"""
        voucher = self.get_voucher(voucher_id)
        if not voucher:
            return False
        
        # Check if voucher can be used
        if not voucher.can_be_used_for_value(transaction_value):
            return False
        
        # Mark voucher as used
        if voucher.mark_as_used(transaction_id):
            # Remove voucher from wallet
            wallet = self.wallet_manager.get_wallet(voucher.issued_to_wallet_id)
            if wallet:
                wallet.use_voucher()
            return True
        
        return False
    
    def verify_voucher_signature(self, voucher_id: str) -> bool:
        """Verify voucher signature (mock verification)"""
        voucher = self.get_voucher(voucher_id)
        if not voucher:
            return False
        
        # Recreate voucher data for verification
        voucher_data = {
            'voucher_id': voucher.voucher_id,
            'value_limit': voucher.value_limit,
            'issued_to_wallet_id': voucher.issued_to_wallet_id,
            'issued_by': voucher.issued_by,
            'issue_timestamp': voucher.issue_timestamp
        }
        
        expected_signature = self._generate_aml_signature(voucher_data)
        return voucher.signature == expected_signature
    
    def get_vouchers_by_wallet(self, wallet_id: str) -> List[Voucher]:
        """Get all vouchers issued to a wallet"""
        return [voucher for voucher in self.vouchers.values() 
                if voucher.issued_to_wallet_id == wallet_id]
    
    def get_available_vouchers_by_wallet(self, wallet_id: str) -> List[Voucher]:
        """Get available (unused) vouchers for a wallet"""
        return [voucher for voucher in self.get_vouchers_by_wallet(wallet_id) 
                if not voucher.is_used]
    
    def list_all_vouchers(self) -> List[Voucher]:
        """List all vouchers in the system"""
        return list(self.vouchers.values())
    
    def get_used_vouchers(self) -> List[Voucher]:
        """Get all used vouchers"""
        return [voucher for voucher in self.vouchers.values() if voucher.is_used]
    
    def get_unused_vouchers(self) -> List[Voucher]:
        """Get all unused vouchers"""
        return [voucher for voucher in self.vouchers.values() if not voucher.is_used] 