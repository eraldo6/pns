"""
AML Compliance and Logging System
Handles transaction legality checks and regulatory reporting
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ComplianceStatus(Enum):
    """Compliance check status"""
    APPROVED = "approved"
    FLAGGED = "flagged"
    REJECTED = "rejected"


@dataclass
class ComplianceResult:
    """Result of a compliance check"""
    is_approved: bool
    status: ComplianceStatus
    reason: Optional[str] = None
    risk_score: float = 0.0
    requires_escalation: bool = False


@dataclass
class AMLEntry:
    """Entry in the AML registry"""
    transaction_id: str
    sender_wallet_id: str
    receiver_wallet_id: str
    token_id: str
    amount: int
    timestamp: str
    reason: str
    risk_score: float
    escalated: bool = False
    authority_notified: bool = False
    
    def to_dict(self) -> Dict:
        """Convert AML entry to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'sender_wallet_id': self.sender_wallet_id,
            'receiver_wallet_id': self.receiver_wallet_id,
            'token_id': self.token_id,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'reason': self.reason,
            'risk_score': self.risk_score,
            'escalated': self.escalated,
            'authority_notified': self.authority_notified
        }


class ComplianceManager:
    """Manages AML compliance checks and regulatory reporting"""
    
    def __init__(self):
        self.aml_registry: List[AMLEntry] = []
        self.compliance_rules = {
            'high_value_threshold': 100,  # €100 threshold
            'suspicious_patterns': [],
            'risk_factors': {}
        }
        self.authority_contacted = False
    
    def check_transaction(self, transaction, token) -> ComplianceResult:
        """Check transaction for AML compliance"""
        risk_score = 0.0
        reasons = []
        
        # Rule 1: High value transactions (>€100)
        if token.value > self.compliance_rules['high_value_threshold']:
            risk_score += 0.7
            reasons.append(f"High value transaction: €{token.value}")
        
        # Rule 2: Non-anonymous transactions (no voucher used)
        if not transaction.is_anonymous:
            risk_score += 0.3
            reasons.append("Non-anonymous transaction")
        
        # Rule 3: Check for suspicious patterns (simplified)
        if self._check_suspicious_patterns(transaction, token):
            risk_score += 0.5
            reasons.append("Suspicious transaction pattern detected")
        
        # Determine compliance status
        if risk_score >= 0.8:
            status = ComplianceStatus.FLAGGED
            is_approved = True  # Allow but flag for monitoring
        elif risk_score >= 0.5:
            status = ComplianceStatus.FLAGGED
            is_approved = True
        else:
            status = ComplianceStatus.APPROVED
            is_approved = True
        
        # Create AML entry if flagged
        if status == ComplianceStatus.FLAGGED:
            self._create_aml_entry(transaction, token, risk_score, reasons)
        
        return ComplianceResult(
            is_approved=is_approved,
            status=status,
            reason="; ".join(reasons) if reasons else None,
            risk_score=risk_score,
            requires_escalation=risk_score >= 0.8
        )
    
    def _check_suspicious_patterns(self, transaction, token) -> bool:
        """Check for suspicious transaction patterns"""
        # Simplified pattern detection
        # In a real system, this would use ML models and historical data
        
        # Pattern 1: Multiple high-value transactions in short time
        recent_transactions = self._get_recent_transactions(transaction.sender_wallet_id, hours=24)
        high_value_count = sum(1 for tx in recent_transactions if tx.get('amount', 0) > 50)
        
        if high_value_count > 3:
            return True
        
        # Pattern 2: Unusual transaction times (simplified)
        # Pattern 3: Geographic anomalies (not implemented in this mock)
        
        return False
    
    def _get_recent_transactions(self, wallet_id: str, hours: int = 24) -> List[Dict]:
        """Get recent transactions for a wallet (mock implementation)"""
        # In a real system, this would query the transaction database
        # For now, return empty list
        return []
    
    def _create_aml_entry(self, transaction, token, risk_score: float, reasons: List[str]):
        """Create an entry in the AML registry"""
        aml_entry = AMLEntry(
            transaction_id=transaction.transaction_id,
            sender_wallet_id=transaction.sender_wallet_id,
            receiver_wallet_id=transaction.receiver_wallet_id,
            token_id=transaction.token_id,
            amount=token.value,
            timestamp=transaction.timestamp or datetime.now().isoformat(),
            reason="; ".join(reasons),
            risk_score=risk_score
        )
        
        self.aml_registry.append(aml_entry)
        
        # Simulate escalation to authority for high-risk transactions
        if risk_score >= 0.8:
            aml_entry.escalated = True
            self._escalate_to_authority(aml_entry)
    
    def _escalate_to_authority(self, aml_entry: AMLEntry):
        """Simulate escalation to regulatory authority"""
        aml_entry.authority_notified = True
        self.authority_contacted = True
        
        # In a real system, this would send notifications to regulatory bodies
        print(f"🚨 HIGH RISK TRANSACTION ESCALATED TO AUTHORITY:")
        print(f"   Transaction ID: {aml_entry.transaction_id}")
        print(f"   Amount: €{aml_entry.amount}")
        print(f"   Risk Score: {aml_entry.risk_score}")
        print(f"   Reason: {aml_entry.reason}")
    
    def get_aml_entries(self) -> List[AMLEntry]:
        """Get all AML registry entries"""
        return self.aml_registry.copy()
    
    def get_flagged_transactions(self) -> List[AMLEntry]:
        """Get all flagged transactions"""
        return [entry for entry in self.aml_registry if entry.risk_score > 0.5]
    
    def get_high_risk_transactions(self) -> List[AMLEntry]:
        """Get high-risk transactions (risk score >= 0.8)"""
        return [entry for entry in self.aml_registry if entry.risk_score >= 0.8]
    
    def get_escalated_transactions(self) -> List[AMLEntry]:
        """Get transactions that were escalated to authority"""
        return [entry for entry in self.aml_registry if entry.escalated]
    
    def export_aml_report(self, filename: str = None) -> str:
        """Export AML registry to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aml_report_{timestamp}.json"
        
        report_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_entries': len(self.aml_registry),
            'high_risk_count': len(self.get_high_risk_transactions()),
            'escalated_count': len(self.get_escalated_transactions()),
            'entries': [entry.to_dict() for entry in self.aml_registry]
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return filename
    
    def get_compliance_statistics(self) -> Dict:
        """Get compliance statistics"""
        total_entries = len(self.aml_registry)
        high_risk = len(self.get_high_risk_transactions())
        escalated = len(self.get_escalated_transactions())
        
        return {
            'total_flagged_transactions': total_entries,
            'high_risk_transactions': high_risk,
            'escalated_transactions': escalated,
            'authority_contacted': self.authority_contacted,
            'average_risk_score': sum(entry.risk_score for entry in self.aml_registry) / total_entries if total_entries > 0 else 0
        } 