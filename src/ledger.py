"""
Privacy Ledger / Audit Layer
Stores transactions with privacy-preserving features
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LedgerEntryType(Enum):
    """Types of ledger entries"""
    ANONYMOUS = "anonymous"
    NON_ANONYMOUS = "non_anonymous"
    AML_FLAGGED = "aml_flagged"


@dataclass
class LedgerEntry:
    """Entry in the privacy ledger"""
    entry_id: str
    transaction_id: str
    sender_wallet_id: str
    receiver_wallet_id: str
    token_id: str
    value: int
    is_anonymous: bool
    entry_type: LedgerEntryType
    timestamp: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata if not provided"""
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'entry_id': self.entry_id,
            'transaction_id': self.transaction_id,
            'sender_wallet_id': self.sender_wallet_id,
            'receiver_wallet_id': self.receiver_wallet_id,
            'token_id': self.token_id,
            'value': self.value,
            'is_anonymous': self.is_anonymous,
            'entry_type': self.entry_type.value,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


class LedgerManager:
    """Manages the privacy ledger and audit capabilities"""
    
    def __init__(self, ledger_file: str = "privacy_ledger.json"):
        self.ledger_file = ledger_file
        self.entries: Dict[str, LedgerEntry] = {}
        self.entry_counter = 0
        self.token_manager = None  # Will be set by main system
        self._load_ledger()
    
    def _load_ledger(self):
        """Load ledger from file if it exists"""
        try:
            with open(self.ledger_file, 'r') as f:
                data = json.load(f)
                self.entries = {}
                for entry_data in data.get('entries', []):
                    entry = LedgerEntry(
                        entry_id=entry_data['entry_id'],
                        transaction_id=entry_data['transaction_id'],
                        sender_wallet_id=entry_data['sender_wallet_id'],
                        receiver_wallet_id=entry_data['receiver_wallet_id'],
                        token_id=entry_data['token_id'],
                        value=entry_data['value'],
                        is_anonymous=entry_data['is_anonymous'],
                        entry_type=LedgerEntryType(entry_data['entry_type']),
                        timestamp=entry_data['timestamp'],
                        metadata=entry_data.get('metadata', {})
                    )
                    self.entries[entry.entry_id] = entry
                    self.entry_counter = max(self.entry_counter, int(entry.entry_id) + 1)
        except FileNotFoundError:
            # Create new ledger file
            self._save_ledger()
    
    def _save_ledger(self):
        """Save ledger to file"""
        data = {
            'ledger_info': {
                'created': datetime.now().isoformat(),
                'total_entries': len(self.entries),
                'anonymous_count': len(self.get_anonymous_entries()),
                'non_anonymous_count': len(self.get_non_anonymous_entries()),
                'aml_flagged_count': len(self.get_aml_flagged_entries())
            },
            'entries': [entry.to_dict() for entry in self.entries.values()]
        }
        
        with open(self.ledger_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def store_transaction(self, transaction) -> str:
        """Store a transaction in the ledger"""
        entry_id = str(self.entry_counter)
        self.entry_counter += 1
        
        # Determine entry type
        if transaction.aml_flagged:
            entry_type = LedgerEntryType.AML_FLAGGED
        elif transaction.is_anonymous:
            entry_type = LedgerEntryType.ANONYMOUS
        else:
            entry_type = LedgerEntryType.NON_ANONYMOUS
        
        # Get token value from token manager
        token_value = 0
        if hasattr(self, 'token_manager') and self.token_manager:
            token = self.token_manager.get_token(transaction.token_id)
            if token:
                token_value = token.value
        
        entry = LedgerEntry(
            entry_id=entry_id,
            transaction_id=transaction.transaction_id,
            sender_wallet_id=transaction.sender_wallet_id,
            receiver_wallet_id=transaction.receiver_wallet_id,
            token_id=transaction.token_id,
            value=token_value,
            is_anonymous=transaction.is_anonymous,
            entry_type=entry_type,
            timestamp=transaction.timestamp or datetime.now().isoformat(),
            metadata={
                'voucher_id': transaction.voucher_id,
                'status': transaction.status.value,
                'aml_reason': transaction.aml_reason
            }
        )
        
        self.entries[entry_id] = entry
        self._save_ledger()
        
        return entry_id
    
    def get_entry(self, entry_id: str) -> Optional[LedgerEntry]:
        """Get ledger entry by ID"""
        return self.entries.get(entry_id)
    
    def get_entries_by_transaction(self, transaction_id: str) -> List[LedgerEntry]:
        """Get all entries for a specific transaction"""
        return [entry for entry in self.entries.values() 
                if entry.transaction_id == transaction_id]
    
    def get_entries_by_wallet(self, wallet_id: str) -> List[LedgerEntry]:
        """Get all entries involving a wallet"""
        return [entry for entry in self.entries.values() 
                if entry.sender_wallet_id == wallet_id or entry.receiver_wallet_id == wallet_id]
    
    def get_anonymous_entries(self) -> List[LedgerEntry]:
        """Get all anonymous entries"""
        return [entry for entry in self.entries.values() 
                if entry.entry_type == LedgerEntryType.ANONYMOUS]
    
    def get_non_anonymous_entries(self) -> List[LedgerEntry]:
        """Get all non-anonymous entries"""
        return [entry for entry in self.entries.values() 
                if entry.entry_type == LedgerEntryType.NON_ANONYMOUS]
    
    def get_aml_flagged_entries(self) -> List[LedgerEntry]:
        """Get all AML-flagged entries"""
        return [entry for entry in self.entries.values() 
                if entry.entry_type == LedgerEntryType.AML_FLAGGED]
    
    def get_entries_by_value_range(self, min_value: int, max_value: int) -> List[LedgerEntry]:
        """Get entries within a value range"""
        return [entry for entry in self.entries.values() 
                if min_value <= entry.value <= max_value]
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> List[LedgerEntry]:
        """Get entries within a date range"""
        return [entry for entry in self.entries.values() 
                if start_date <= entry.timestamp <= end_date]
    
    def get_ledger_statistics(self) -> Dict:
        """Get comprehensive ledger statistics"""
        total_entries = len(self.entries)
        anonymous_entries = self.get_anonymous_entries()
        non_anonymous_entries = self.get_non_anonymous_entries()
        aml_flagged_entries = self.get_aml_flagged_entries()
        
        total_value = sum(entry.value for entry in self.entries.values())
        anonymous_value = sum(entry.value for entry in anonymous_entries)
        non_anonymous_value = sum(entry.value for entry in non_anonymous_entries)
        
        return {
            'total_entries': total_entries,
            'anonymous_entries': len(anonymous_entries),
            'non_anonymous_entries': len(non_anonymous_entries),
            'aml_flagged_entries': len(aml_flagged_entries),
            'total_value': total_value,
            'anonymous_value': anonymous_value,
            'non_anonymous_value': non_anonymous_value,
            'anonymous_percentage': (len(anonymous_entries) / total_entries * 100) if total_entries > 0 else 0,
            'value_anonymous_percentage': (anonymous_value / total_value * 100) if total_value > 0 else 0
        }
    
    def export_aml_loggable_transactions(self, filename: str = None) -> str:
        """Export transactions that should be logged for AML purposes"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aml_loggable_transactions_{timestamp}.json"
        
        # Get non-anonymous and AML-flagged entries
        aml_entries = self.get_non_anonymous_entries() + self.get_aml_flagged_entries()
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_aml_entries': len(aml_entries),
            'entries': [entry.to_dict() for entry in aml_entries]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def export_anonymous_volume_report(self, filename: str = None) -> str:
        """Export anonymous vs non-anonymous volume report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"volume_report_{timestamp}.json"
        
        stats = self.get_ledger_statistics()
        
        report_data = {
            'report_timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'anonymous_entries': [entry.to_dict() for entry in self.get_anonymous_entries()],
            'non_anonymous_entries': [entry.to_dict() for entry in self.get_non_anonymous_entries()]
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return filename
    
    def query_ledger(self, query_params: Dict) -> List[LedgerEntry]:
        """Query ledger with various filters"""
        results = list(self.entries.values())
        
        # Filter by entry type
        if 'entry_type' in query_params:
            entry_type = LedgerEntryType(query_params['entry_type'])
            results = [entry for entry in results if entry.entry_type == entry_type]
        
        # Filter by wallet
        if 'wallet_id' in query_params:
            wallet_id = query_params['wallet_id']
            results = [entry for entry in results 
                      if entry.sender_wallet_id == wallet_id or entry.receiver_wallet_id == wallet_id]
        
        # Filter by value range
        if 'min_value' in query_params and 'max_value' in query_params:
            min_val = query_params['min_value']
            max_val = query_params['max_value']
            results = [entry for entry in results if min_val <= entry.value <= max_val]
        
        # Filter by date range
        if 'start_date' in query_params and 'end_date' in query_params:
            start_date = query_params['start_date']
            end_date = query_params['end_date']
            results = [entry for entry in results if start_date <= entry.timestamp <= end_date]
        
        return results
    
    def get_ledger_hash(self) -> str:
        """Get cryptographic hash of the ledger for integrity verification"""
        # Create a hash of all entries for integrity checking
        entries_data = []
        for entry in sorted(self.entries.values(), key=lambda x: x.entry_id):
            entries_data.append(entry.to_dict())
        
        data_str = json.dumps(entries_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest() 