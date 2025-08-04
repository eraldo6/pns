"""
Token Representation and Issuance System
Handles token creation, ownership, and transfer
"""

import uuid
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class TokenValue(Enum):
    """Predefined token values in euros"""
    ONE_EURO = 1
    FIVE_EURO = 5
    TEN_EURO = 10
    TWENTY_EURO = 20
    FIFTY_EURO = 50
    HUNDRED_EURO = 100


@dataclass
class Token:
    """Digital token representing monetary value"""
    token_id: str
    value: int  # Value in euros
    owner_wallet_id: str
    issued_by: str = "ECB"  # Issuing authority
    issue_timestamp: Optional[str] = None
    
    def __post_init__(self):
        """Validate token after creation"""
        if not self.token_id or self.value <= 0 or not self.owner_wallet_id:
            raise ValueError("Token must have valid ID, positive value, and owner")
    
    def transfer_ownership(self, new_owner_wallet_id: str) -> bool:
        """Transfer token ownership to new wallet"""
        if new_owner_wallet_id:
            self.owner_wallet_id = new_owner_wallet_id
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert token to dictionary for serialization"""
        return {
            'token_id': self.token_id,
            'value': self.value,
            'owner_wallet_id': self.owner_wallet_id,
            'issued_by': self.issued_by,
            'issue_timestamp': self.issue_timestamp
        }


class TokenManager:
    """Manages token creation, issuance, and tracking"""
    
    def __init__(self):
        self.tokens: Dict[str, Token] = {}
        self.wallet_manager = None  # Will be set by main system
    
    def set_wallet_manager(self, wallet_manager):
        """Set reference to wallet manager"""
        self.wallet_manager = wallet_manager
    
    def issue_token(self, value: int, owner_wallet_id: str) -> Token:
        """Issue new token to a wallet (mock ECB issuing)"""
        if not self.wallet_manager or not self.wallet_manager.wallet_exists(owner_wallet_id):
            raise ValueError(f"Wallet {owner_wallet_id} does not exist")
        
        token_id = str(uuid.uuid4())
        token = Token(
            token_id=token_id,
            value=value,
            owner_wallet_id=owner_wallet_id
        )
        
        self.tokens[token_id] = token
        
        # Add token to wallet balance
        wallet = self.wallet_manager.get_wallet(owner_wallet_id)
        if wallet:
            wallet.add_token(token_id)
        
        return token
    
    def get_token(self, token_id: str) -> Optional[Token]:
        """Retrieve token by ID"""
        return self.tokens.get(token_id)
    
    def transfer_token(self, token_id: str, sender_wallet_id: str, receiver_wallet_id: str) -> bool:
        """Transfer token ownership between wallets"""
        token = self.get_token(token_id)
        if not token:
            return False
        
        # Verify sender owns the token
        if token.owner_wallet_id != sender_wallet_id:
            return False
        
        # Verify both wallets exist
        if not self.wallet_manager:
            return False
        
        if not (self.wallet_manager.wallet_exists(sender_wallet_id) and 
                self.wallet_manager.wallet_exists(receiver_wallet_id)):
            return False
        
        # Remove from sender wallet
        sender_wallet = self.wallet_manager.get_wallet(sender_wallet_id)
        if sender_wallet:
            sender_wallet.remove_token(token_id)
        
        # Add to receiver wallet
        receiver_wallet = self.wallet_manager.get_wallet(receiver_wallet_id)
        if receiver_wallet:
            receiver_wallet.add_token(token_id)
        
        # Update token ownership
        token.transfer_ownership(receiver_wallet_id)
        
        return True
    
    def get_tokens_by_owner(self, wallet_id: str) -> List[Token]:
        """Get all tokens owned by a wallet"""
        return [token for token in self.tokens.values() if token.owner_wallet_id == wallet_id]
    
    def get_total_value_by_owner(self, wallet_id: str) -> int:
        """Get total token value owned by a wallet"""
        return sum(token.value for token in self.get_tokens_by_owner(wallet_id))
    
    def list_all_tokens(self) -> List[Token]:
        """List all tokens in the system"""
        return list(self.tokens.values()) 