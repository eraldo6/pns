"""
Main System Coordinator
Ties all components together and provides system-wide functionality
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List

from wallet import WalletManager
from token_system import TokenManager
from voucher import VoucherManager
from transaction import TransactionEngine
from compliance import ComplianceManager
from ledger import LedgerManager
from offline import OfflineManager
from zkp import ZKPManager
from cli import PrivacyNetworkCLI


class PrivacyNetworkSystem:
    """Main system coordinator for the Privacy Network System"""
    
    def __init__(self):
        """Initialize all system components"""
        print("Initializing Euromask...")
        
        # Initialize all managers
        self.wallet_manager = WalletManager()
        self.token_manager = TokenManager()
        self.voucher_manager = VoucherManager()
        self.compliance_manager = ComplianceManager()
        self.ledger_manager = LedgerManager()
        self.offline_manager = OfflineManager()
        self.zkp_manager = ZKPManager()
        self.transaction_engine = TransactionEngine()
        
        # Set up cross-references between managers
        self._setup_manager_references()
        
        print("System initialized successfully!")
    
    def _setup_manager_references(self):
        """Set up cross-references between managers"""
        # Set wallet manager references
        self.token_manager.set_wallet_manager(self.wallet_manager)
        self.voucher_manager.set_wallet_manager(self.wallet_manager)
        
        # Set manager references for transaction engine
        self.transaction_engine.set_managers(
            self.wallet_manager,
            self.token_manager,
            self.voucher_manager,
            self.compliance_manager,
            self.ledger_manager
        )
        
        # Set manager references for offline manager
        self.offline_manager.set_managers(
            self.wallet_manager,
            self.token_manager,
            self.voucher_manager,
            self.ledger_manager
        )
        
        # Set manager references for ZKP manager
        self.zkp_manager.set_managers(
            self.wallet_manager,
            self.token_manager
        )
        
        # Set token manager reference for ledger manager
        self.ledger_manager.token_manager = self.token_manager
    
    def run_demo(self):
        """Run a comprehensive demonstration of the system"""
        print("\nEuromask - Comprehensive Demo")
        print("=" * 50)
        
        try:
            # 1. Create wallets
            print("1. Creating wallets...")
            wallet1 = self.wallet_manager.create_wallet()
            wallet2 = self.wallet_manager.create_wallet()
            wallet3 = self.wallet_manager.create_wallet()
            print(f"   Created 3 wallets")
            
            # 2. Issue tokens
            print("2. Issuing tokens...")
            token1 = self.token_manager.issue_token(50, wallet1.wallet_id)
            token2 = self.token_manager.issue_token(100, wallet2.wallet_id)
            token3 = self.token_manager.issue_token(25, wallet3.wallet_id)
            print(f"   Issued tokens: €{token1.value}, €{token2.value}, €{token3.value}")
            
            # 3. Issue vouchers
            print("3. Issuing anonymity vouchers...")
            voucher1 = self.voucher_manager.issue_voucher(wallet1.wallet_id, 50)
            voucher2 = self.voucher_manager.issue_voucher(wallet2.wallet_id, 100)
            print(f"   Issued vouchers with limits: €{voucher1.value_limit}, €{voucher2.value_limit}")
            
            # 4. Execute regular transfer
            print("4. Executing regular transfer...")
            tx1 = self.transaction_engine.execute_transfer(wallet1.wallet_id, wallet2.wallet_id, token1.token_id)
            print(f"   Regular transfer completed ({'AML flagged' if tx1.aml_flagged else 'no flags'})")
            
            # 5. Execute anonymous transfer
            print("5. Executing anonymous transfer...")
            tx2 = self.transaction_engine.execute_transfer(wallet2.wallet_id, wallet3.wallet_id, token2.token_id, voucher2.voucher_id)
            print(f"   Anonymous transfer completed")
            
            # 6. Execute high-value transfer (AML flagged)
            print("6. Executing high-value transfer...")
            # Create a high-value token for AML testing
            high_value_token = self.token_manager.issue_token(10000, wallet1.wallet_id)
            tx3 = self.transaction_engine.execute_transfer(wallet1.wallet_id, wallet2.wallet_id, high_value_token.token_id)
            print(f"   High-value transfer completed ({'AML flagged' if tx3.aml_flagged else 'no flags'})")
            
            # 7. Create offline transfer
            print("7. Creating offline transfer...")
            offline_tx = self.offline_manager.create_offline_transaction(wallet3.wallet_id, wallet1.wallet_id, token3.token_id)
            print(f"   Offline transfer created")
            
            # 8. Generate ZKP proof
            print("8. Generating zero-knowledge proof...")
            proof = self.zkp_manager.generate_range_proof(wallet1.wallet_id, 0, 200)
            print(f"   Range proof generated")
            
            # 9. Show system status
            print("9. System Status:")
            self._show_system_status()
            
            print("Demo completed successfully!")
            
        except Exception as e:
            print(f"Demo failed: {e}")
    
    def _show_system_status(self):
        """Show comprehensive system status"""
        wallets = self.wallet_manager.list_wallets()
        tokens = self.token_manager.list_all_tokens()
        vouchers = self.voucher_manager.list_all_vouchers()
        transactions = self.transaction_engine.list_all_transactions()
        aml_entries = self.compliance_manager.get_aml_entries()
        offline_txs = self.offline_manager.list_all_offline_transactions()
        zkp_proofs = self.zkp_manager.list_all_proofs()
        
        total_token_value = sum(token.value for token in tokens)
        available_vouchers = self.voucher_manager.get_unused_vouchers()
        anonymous_transactions = self.transaction_engine.get_anonymous_transactions()
        pending_offline = self.offline_manager.get_pending_offline_transactions()
        
        print(f"   Wallets: {len(wallets)}")
        print(f"   Tokens: {len(tokens)} (€{total_token_value})")
        print(f"   Vouchers: {len(vouchers)} ({len(available_vouchers)} available)")
        print(f"   Transactions: {len(transactions)} ({len(anonymous_transactions)} anonymous)")
        print(f"   AML Flagged: {len(aml_entries)}")
        print(f"   Offline: {len(offline_txs)} ({len(pending_offline)} pending)")
        print(f"   ZKP Proofs: {len(zkp_proofs)}")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        wallets = self.wallet_manager.list_wallets()
        tokens = self.token_manager.list_all_tokens()
        vouchers = self.voucher_manager.list_all_vouchers()
        transactions = self.transaction_engine.list_all_transactions()
        aml_entries = self.compliance_manager.get_aml_entries()
        offline_txs = self.offline_manager.list_all_offline_transactions()
        zkp_proofs = self.zkp_manager.list_all_proofs()
        
        total_token_value = sum(token.value for token in tokens)
        available_vouchers = self.voucher_manager.get_unused_vouchers()
        anonymous_transactions = self.transaction_engine.get_anonymous_transactions()
        pending_offline = self.offline_manager.get_pending_offline_transactions()
        
        return {
            'wallets': len(wallets),
            'tokens': len(tokens),
            'total_token_value': total_token_value,
            'vouchers': len(vouchers),
            'available_vouchers': len(available_vouchers),
            'transactions': len(transactions),
            'anonymous_transactions': len(anonymous_transactions),
            'aml_flagged': len(aml_entries),
            'offline_transactions': len(offline_txs),
            'pending_offline': len(pending_offline),
            'zkp_proofs': len(zkp_proofs)
        }
    
    def export_system_data(self) -> Dict[str, str]:
        """Export all system data to JSON files"""
        print("Exporting system data...")
        
        exported_files = {}
        
        try:
            # Export AML report
            aml_filename = self.compliance_manager.export_aml_report()
            exported_files['AML Report'] = aml_filename
            
            # Export ledger data
            ledger_filename = self.ledger_manager.export_aml_loggable_transactions()
            exported_files['Ledger Export'] = ledger_filename
            
            # Export volume report
            volume_filename = self.ledger_manager.export_anonymous_volume_report()
            exported_files['Volume Report'] = volume_filename
            
            # Export offline transactions
            offline_filename = self.offline_manager.export_offline_transactions()
            exported_files['Offline Transactions'] = offline_filename
            
            # Export ZKP proofs
            zkp_filename = self.zkp_manager.export_zkp_proofs()
            exported_files['ZKP Proofs'] = zkp_filename
            
            print("System data exported:")
            for file_type, filename in exported_files.items():
                print(f"   {file_type}: {filename}")
            
            return exported_files
            
        except Exception as e:
            print(f"Export failed: {e}")
            return {}
    
    def run_cli(self):
        """Run the interactive command-line interface"""
        cli = PrivacyNetworkCLI(self)
        cli.run()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Euromask - Digital Currency with Privacy Features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo                    # Run demonstration
  python main.py --interactive             # Start interactive CLI
  python main.py --demo --interactive      # Run demo then start CLI
        """
    )
    
    parser.add_argument('--demo', action='store_true', help='Run comprehensive demonstration')
    parser.add_argument('--interactive', action='store_true', help='Start interactive command line interface')
    parser.add_argument('--export', action='store_true', help='Export all system data')
    parser.add_argument('--status', action='store_true', help='Show system status')
    
    args = parser.parse_args()
    
    # Initialize system
    system = PrivacyNetworkSystem()
    
    # Handle command line arguments
    if args.demo:
        system.run_demo()
    
    if args.status:
        print("\nSystem Status:")
        print("=" * 30)
        status = system.get_system_status()
        print(f"   Wallets: {status['wallets']}")
        print(f"   Tokens: {status['tokens']} (€{status['total_token_value']})")
        print(f"   Vouchers: {status['vouchers']} ({status['available_vouchers']} available)")
        print(f"   Transactions: {status['transactions']} ({status['anonymous_transactions']} anonymous)")
        print(f"   AML Flagged: {status['aml_flagged']}")
        print(f"   Offline: {status['offline_transactions']} ({status['pending_offline']} pending)")
        print(f"   ZKP Proofs: {status['zkp_proofs']}")
    
    if args.export:
        system.export_system_data()
    
    if args.interactive:
        system.run_cli()
    
    # If no arguments provided, show help
    if not any([args.demo, args.status, args.export, args.interactive]):
        parser.print_help()


if __name__ == "__main__":
    main() 