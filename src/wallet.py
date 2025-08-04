"""
Wallet System Implementation
Handles wallet creation, key management, and transaction signing
"""

import uuid
import hashlib
import secrets
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json


@dataclass
class Wallet:
    """Digital wallet for storing tokens and vouchers"""
    wallet_id: str
    public_key: str
    private_key: str
    token_balance: List[str] = field(default_factory=list)  # List of token IDs
    voucher_balance: int = 0
    
    def __post_init__(self):
        """Validate wallet after creation"""
        if not self.wallet_id or not self.public_key or not self.private_key:
            raise ValueError("Wallet must have valid ID, public key, and private key")
    
    def add_token(self, token_id: str) -> None:
        """Add a token to wallet balance"""
        if token_id not in self.token_balance:
            self.token_balance.append(token_id)
    
    def remove_token(self, token_id: str) -> bool:
        """Remove a token from wallet balance"""
        if token_id in self.token_balance:
            self.token_balance.remove(token_id)
            return True
        return False
    
    def add_voucher(self, count: int = 1) -> None:
        """Add vouchers to wallet"""
        self.voucher_balance += count
    
    def use_voucher(self) -> bool:
        """Use one voucher from wallet"""
        if self.voucher_balance > 0:
            self.voucher_balance -= 1
            return True
        return False
    
    def sign_transaction(self, transaction_data: Dict) -> str:
        """Sign transaction data with private key (simulated)"""
        # In a real implementation, this would use proper cryptographic signing
        data_str = json.dumps(transaction_data, sort_keys=True)
        signature = hashlib.sha256((data_str + self.private_key).encode()).hexdigest()
        return signature
    
    def verify_signature(self, data: Dict, signature: str) -> bool:
        """Verify signature using public key (simulated)"""
        data_str = json.dumps(data, sort_keys=True)
        expected_signature = hashlib.sha256((data_str + self.private_key).encode()).hexdigest()
        return signature == expected_signature
    
    def to_dict(self) -> Dict:
        """Convert wallet to dictionary for serialization"""
        return {
            'wallet_id': self.wallet_id,
            'public_key': self.public_key,
            'token_balance': self.token_balance,
            'voucher_balance': self.voucher_balance
            # Note: private_key is not included for security
        }


class WalletManager:
    """Manages wallet creation and storage"""
    
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}
    
    def create_wallet(self) -> Wallet:
        """Create a new wallet with cryptographic keypair"""
        wallet_id = str(uuid.uuid4())
        
        # Generate cryptographic keypair (simulated)
        private_key = secrets.token_hex(32)
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        
        wallet = Wallet(
            wallet_id=wallet_id,
            public_key=public_key,
            private_key=private_key
        )
        
        self.wallets[wallet_id] = wallet
        return wallet
    
    def get_wallet(self, wallet_id: str) -> Optional[Wallet]:
        """Retrieve wallet by ID"""
        return self.wallets.get(wallet_id)
    
    def list_wallets(self) -> List[Wallet]:
        """List all wallets"""
        return list(self.wallets.values())
    
    def wallet_exists(self, wallet_id: str) -> bool:
        """Check if wallet exists"""
        return wallet_id in self.wallets 