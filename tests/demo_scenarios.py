"""
Demo Scenarios and Tests
Comprehensive test scenarios for the Euromask system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from wallet import WalletManager, Wallet
from token_system import TokenManager, Token
from voucher import VoucherManager, Voucher
from transaction import TransactionEngine, Transaction
from compliance import ComplianceManager
from ledger import LedgerManager
from offline import OfflineManager, OfflineTransaction
from zkp import ZKPManager, ZKPProof


def test_wallet_creation():
    """Test wallet creation and management"""
    print("Testing Wallet Creation...")
    
    wallet_manager = WalletManager()
    
    # Create wallets
    wallet1 = wallet_manager.create_wallet()
    wallet2 = wallet_manager.create_wallet()
    
    assert wallet1.wallet_id != wallet2.wallet_id
    assert wallet1.public_key != wallet2.public_key
    assert len(wallet_manager.list_wallets()) == 2
    
    print("Wallet creation test passed")


def test_token_issuance():
    """Test token issuance and management"""
    print("Testing Token Issuance...")
    
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    token_manager.set_wallet_manager(wallet_manager)
    
    # Create wallet and issue tokens
    wallet = wallet_manager.create_wallet()
    token1 = token_manager.issue_token(50, wallet.wallet_id)
    token2 = token_manager.issue_token(100, wallet.wallet_id)
    
    assert token1.value == 50
    assert token2.value == 100
    assert token1.owner_wallet_id == wallet.wallet_id
    assert token2.owner_wallet_id == wallet.wallet_id
    
    # Check wallet balance
    wallet_tokens = token_manager.get_tokens_by_owner(wallet.wallet_id)
    assert len(wallet_tokens) == 2
    assert token_manager.get_total_value_by_owner(wallet.wallet_id) == 150
    
    print("Token issuance test passed")


def test_voucher_system():
    """Test voucher issuance and redemption"""
    print("Testing Voucher System...")
    
    wallet_manager = WalletManager()
    voucher_manager = VoucherManager()
    voucher_manager.set_wallet_manager(wallet_manager)
    
    # Create wallet and issue voucher
    wallet = wallet_manager.create_wallet()
    voucher = voucher_manager.issue_voucher(wallet.wallet_id, 100)
    
    assert voucher.value_limit == 100
    assert voucher.issued_to_wallet_id == wallet.wallet_id
    assert not voucher.is_used
    
    # Test voucher verification
    assert voucher_manager.verify_voucher_signature(voucher.voucher_id)
    
    # Test voucher redemption
    transaction_id = "test_transaction_123"
    assert voucher_manager.redeem_voucher(voucher.voucher_id, transaction_id, 50)
    assert voucher.is_used
    assert voucher.used_in_transaction == transaction_id
    
    print("Voucher system test passed")


def test_regular_transfer():
    """Test regular (non-anonymous) token transfer"""
    print("Testing Regular Transfer...")
    
    # Initialize managers
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    voucher_manager = VoucherManager()
    compliance_manager = ComplianceManager()
    ledger_manager = LedgerManager()
    
    token_manager.set_wallet_manager(wallet_manager)
    voucher_manager.set_wallet_manager(wallet_manager)
    ledger_manager.token_manager = token_manager
    
    transaction_engine = TransactionEngine()
    transaction_engine.set_managers(
        wallet_manager, token_manager, voucher_manager, 
        compliance_manager, ledger_manager
    )
    
    # Create wallets and issue token
    sender = wallet_manager.create_wallet()
    receiver = wallet_manager.create_wallet()
    token = token_manager.issue_token(75, sender.wallet_id)
    
    # Execute transfer
    transaction = transaction_engine.execute_transfer(
        sender.wallet_id, receiver.wallet_id, token.token_id
    )
    
    assert transaction.status.value == "completed"
    assert not transaction.is_anonymous
    assert token.owner_wallet_id == receiver.wallet_id
    
    # Check wallet balances
    sender_tokens = token_manager.get_tokens_by_owner(sender.wallet_id)
    receiver_tokens = token_manager.get_tokens_by_owner(receiver.wallet_id)
    assert len(sender_tokens) == 0
    assert len(receiver_tokens) == 1
    
    print("Regular transfer test passed")


def test_anonymous_transfer():
    """Test anonymous token transfer with voucher"""
    print("Testing Anonymous Transfer...")
    
    # Initialize managers
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    voucher_manager = VoucherManager()
    compliance_manager = ComplianceManager()
    ledger_manager = LedgerManager()
    
    token_manager.set_wallet_manager(wallet_manager)
    voucher_manager.set_wallet_manager(wallet_manager)
    ledger_manager.token_manager = token_manager
    
    transaction_engine = TransactionEngine()
    transaction_engine.set_managers(
        wallet_manager, token_manager, voucher_manager, 
        compliance_manager, ledger_manager
    )
    
    # Create wallets, issue token and voucher
    sender = wallet_manager.create_wallet()
    receiver = wallet_manager.create_wallet()
    token = token_manager.issue_token(50, sender.wallet_id)
    voucher = voucher_manager.issue_voucher(sender.wallet_id, 100)
    
    # Execute anonymous transfer
    transaction = transaction_engine.execute_transfer(
        sender.wallet_id, receiver.wallet_id, token.token_id, voucher.voucher_id
    )
    
    assert transaction.status.value == "completed"
    assert transaction.is_anonymous
    assert voucher.is_used
    assert token.owner_wallet_id == receiver.wallet_id
    
    print("Anonymous transfer test passed")


def test_offline_transfer():
    """Test offline transaction creation and synchronization"""
    print("Testing Offline Transfer...")
    
    # Initialize managers
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    voucher_manager = VoucherManager()
    ledger_manager = LedgerManager()
    
    token_manager.set_wallet_manager(wallet_manager)
    voucher_manager.set_wallet_manager(wallet_manager)
    ledger_manager.token_manager = token_manager
    
    offline_manager = OfflineManager()
    offline_manager.set_managers(
        wallet_manager, token_manager, voucher_manager, ledger_manager
    )
    
    # Create wallets and issue token
    sender = wallet_manager.create_wallet()
    receiver = wallet_manager.create_wallet()
    token = token_manager.issue_token(25, sender.wallet_id)
    
    # Create offline transaction
    offline_tx = offline_manager.create_offline_transaction(
        sender.wallet_id, receiver.wallet_id, token.token_id
    )
    
    assert offline_tx.status.value == "pending"
    assert offline_tx.sender_wallet_id == sender.wallet_id
    assert offline_tx.receiver_wallet_id == receiver.wallet_id
    assert offline_tx.token_id == token.token_id
    
    # Simulate signing (mock signatures)
    # Get actual signatures from wallets
    sender_wallet = wallet_manager.get_wallet(sender.wallet_id)
    receiver_wallet = wallet_manager.get_wallet(receiver.wallet_id)
    
    tx_data = {
        'offline_id': offline_tx.offline_id,
        'sender_wallet_id': offline_tx.sender_wallet_id,
        'receiver_wallet_id': offline_tx.receiver_wallet_id,
        'token_id': offline_tx.token_id,
        'value': offline_tx.value,
        'voucher_id': offline_tx.voucher_id,
        'is_anonymous': offline_tx.is_anonymous
    }
    
    sender_signature = sender_wallet.sign_transaction(tx_data)
    receiver_signature = receiver_wallet.sign_transaction(tx_data)
    
    assert offline_manager.sign_offline_transaction(offline_tx.offline_id, sender.wallet_id, sender_signature)
    assert offline_manager.sign_offline_transaction(offline_tx.offline_id, receiver.wallet_id, receiver_signature)
    
    # Sync with ledger
    assert offline_manager.sync_with_ledger(offline_tx.offline_id)
    assert offline_tx.status.value == "synced"
    
    print("Offline transfer test passed")


def test_compliance_monitoring():
    """Test AML compliance monitoring"""
    print("Testing Compliance Monitoring...")
    
    compliance_manager = ComplianceManager()
    
    # Create mock transaction and token for testing
    class MockTransaction:
        def __init__(self):
            self.transaction_id = "test_tx_123"
            self.sender_wallet_id = "test_sender"
            self.receiver_wallet_id = "test_receiver"
            self.token_id = "test_token_123"
            self.timestamp = "2025-01-01T12:00:00"
            self.is_anonymous = False
    
    class MockToken:
        def __init__(self, value):
            self.value = value
    
    # Test high-value transaction
    high_value_tx = MockTransaction()
    high_value_token = MockToken(150)  # Above €100 threshold
    
    result = compliance_manager.check_transaction(high_value_tx, high_value_token)
    assert result.status.value == "flagged"
    assert result.risk_score > 0.5
    
    # Test anonymous transaction
    anonymous_tx = MockTransaction()
    anonymous_tx.is_anonymous = True
    low_value_token = MockToken(50)
    
    result = compliance_manager.check_transaction(anonymous_tx, low_value_token)
    # Anonymous transactions with low value should be approved, not flagged
    assert result.status.value == "approved"
    
    # Check AML entries
    aml_entries = compliance_manager.get_aml_entries()
    assert len(aml_entries) > 0
    
    print("Compliance monitoring test passed")


def test_ledger_privacy():
    """Test privacy ledger functionality"""
    print("Testing Ledger Privacy...")
    
    ledger_manager = LedgerManager()
    
    # Create mock transaction for testing
    class MockTransaction:
        def __init__(self):
            self.transaction_id = "test_tx_123"
            self.sender_wallet_id = "sender_123"
            self.receiver_wallet_id = "receiver_456"
            self.token_id = "token_789"
            self.voucher_id = None
            self.is_anonymous = True
            self.aml_flagged = False
            self.aml_reason = None
            self.timestamp = "2025-01-01T12:00:00"
            self.status = type('Status', (), {'value': 'completed'})()
    
    # Store transaction
    entry_id = ledger_manager.store_transaction(MockTransaction())
    assert entry_id is not None
    
    # Check ledger statistics
    stats = ledger_manager.get_ledger_statistics()
    assert stats['total_entries'] > 0
    assert stats['anonymous_entries'] > 0
    
    print("Ledger privacy test passed")


def test_zkp_system():
    """Test zero-knowledge proof system"""
    print("Testing ZKP System...")
    
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    zkp_manager = ZKPManager()
    
    token_manager.set_wallet_manager(wallet_manager)
    zkp_manager.set_managers(wallet_manager, token_manager)
    
    # Create wallet and issue tokens
    wallet = wallet_manager.create_wallet()
    token1 = token_manager.issue_token(50, wallet.wallet_id)
    token2 = token_manager.issue_token(75, wallet.wallet_id)
    
    # Generate range proof
    proof = zkp_manager.generate_range_proof(wallet.wallet_id, 0, 200)
    assert proof.proof_type.value == "range_proof"
    assert proof.statement['wallet_id'] == wallet.wallet_id
    
    # Verify proof
    assert zkp_manager.verify_range_proof(proof.proof_id)
    assert proof.verified
    
    # Generate equality proof
    proof2 = zkp_manager.generate_equality_proof(wallet.wallet_id, token1.token_id, 50)
    assert proof2.proof_type.value == "equality_proof"
    
    # Verify equality proof
    assert zkp_manager.verify_equality_proof(proof2.proof_id)
    
    print("ZKP system test passed")


def test_comprehensive_demo():
    """Test comprehensive system integration"""
    print("Testing Comprehensive System Integration...")
    
    # Initialize all managers
    wallet_manager = WalletManager()
    token_manager = TokenManager()
    voucher_manager = VoucherManager()
    compliance_manager = ComplianceManager()
    ledger_manager = LedgerManager()
    offline_manager = OfflineManager()
    zkp_manager = ZKPManager()
    
    # Set up cross-references
    token_manager.set_wallet_manager(wallet_manager)
    voucher_manager.set_wallet_manager(wallet_manager)
    ledger_manager.token_manager = token_manager
    
    transaction_engine = TransactionEngine()
    transaction_engine.set_managers(
        wallet_manager, token_manager, voucher_manager, 
        compliance_manager, ledger_manager
    )
    
    offline_manager.set_managers(
        wallet_manager, token_manager, voucher_manager, ledger_manager
    )
    
    zkp_manager.set_managers(wallet_manager, token_manager)
    
    # Create wallets
    wallet1 = wallet_manager.create_wallet()
    wallet2 = wallet_manager.create_wallet()
    wallet3 = wallet_manager.create_wallet()
    
    # Issue tokens
    token1 = token_manager.issue_token(50, wallet1.wallet_id)
    token2 = token_manager.issue_token(100, wallet2.wallet_id)
    token3 = token_manager.issue_token(25, wallet3.wallet_id)
    
    # Issue vouchers
    voucher1 = voucher_manager.issue_voucher(wallet1.wallet_id, 50)
    voucher2 = voucher_manager.issue_voucher(wallet2.wallet_id, 100)
    
    # Execute transfers
    tx1 = transaction_engine.execute_transfer(wallet1.wallet_id, wallet2.wallet_id, token1.token_id)
    tx2 = transaction_engine.execute_transfer(wallet2.wallet_id, wallet3.wallet_id, token2.token_id, voucher2.voucher_id)
    
    # Create offline transaction
    offline_tx = offline_manager.create_offline_transaction(wallet3.wallet_id, wallet1.wallet_id, token3.token_id)
    
    # Generate ZKP proof
    proof = zkp_manager.generate_range_proof(wallet1.wallet_id, 0, 200)
    
    # Verify all components
    assert len(wallet_manager.list_wallets()) == 3
    assert len(token_manager.list_all_tokens()) == 3
    assert len(voucher_manager.list_all_vouchers()) == 2
    assert len(transaction_engine.list_all_transactions()) == 2
    assert len(offline_manager.list_all_offline_transactions()) == 1
    assert len(zkp_manager.list_all_proofs()) == 1
    
    # Check transaction types
    anonymous_txs = transaction_engine.get_anonymous_transactions()
    assert len(anonymous_txs) == 1
    
    # Check voucher usage
    used_vouchers = voucher_manager.get_used_vouchers()
    assert len(used_vouchers) == 1
    
    print("Comprehensive system integration test passed")


def run_all_tests():
    """Run all test scenarios"""
    print("🚀 Running Privacy Network System Tests")
    print("=" * 50)
    
    tests = [
        test_wallet_creation,
        test_token_issuance,
        test_voucher_system,
        test_regular_transfer,
        test_anonymous_transfer,
        test_offline_transfer,
        test_compliance_monitoring,
        test_ledger_privacy,
        test_zkp_system,
        test_comprehensive_demo
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"Test failed: {e}")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests() 